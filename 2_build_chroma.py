"""
Step 2 - Build the vector index for classic RAG.

PDF pages -> text chunks -> embeddings (bge-small) -> ChromaDB (saved in chroma_db/)

Run (with the LLM server running):  .venv\\Scripts\\python.exe 2_build_chroma.py
"""
import chromadb
from pypdf import PdfReader

import config
from rag import llm


def chunk_text(text, size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP):
    """Split text into overlapping pieces of about `size` characters (breaking at spaces)."""
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            end = text.rfind(" ", start, end) + 1 or end   # don't cut words in half
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = end - overlap
    return chunks


def load_chunks():
    """Read every PDF page and split it into chunks with metadata (city, page, source)."""
    ids, texts, metas = [], [], []
    for pdf in sorted(config.PDF_DIR.glob("*.pdf")):
        city = pdf.stem.replace("_Travel_Guide", "").replace("_", " ")
        for page_no, page in enumerate(PdfReader(pdf).pages, start=1):
            page_text = " ".join(page.extract_text().split())   # tidy whitespace
            for i, chunk in enumerate(chunk_text(page_text)):
                # A small header makes every chunk self-explanatory, even mid-page
                ids.append(f"{city}-p{page_no}-c{i}")
                texts.append(f"[{city} travel guide, page {page_no}] {chunk}")
                metas.append({"city": city, "page": page_no, "source": pdf.name})
    return ids, texts, metas


if __name__ == "__main__":
    ids, texts, metas = load_chunks()
    print(f"Loaded {len(texts)} chunks from {len(list(config.PDF_DIR.glob('*.pdf')))} PDFs")

    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    if config.CHROMA_COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(config.CHROMA_COLLECTION)          # start fresh
    collection = client.create_collection(config.CHROMA_COLLECTION, metadata={"hnsw:space": "cosine"})

    batch = 16
    for i in range(0, len(texts), batch):
        collection.add(ids=ids[i:i + batch],
                       documents=texts[i:i + batch],
                       metadatas=metas[i:i + batch],
                       embeddings=llm.embed(texts[i:i + batch]))
        print(f"  embedded {min(i + batch, len(texts))}/{len(texts)}")

    print(f"Done. Collection '{config.CHROMA_COLLECTION}' now holds {collection.count()} chunks.")
