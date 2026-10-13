"""
basic_rag.py - Classic RAG (Retrieval-Augmented Generation).

    question --> RETRIEVER --> AUGMENTATION --> GENERATION --> answer
                 (ChromaDB)    (build prompt)   (LLM writes)
"""
from functools import lru_cache

import chromadb

import config
from rag import llm


@lru_cache
def _collection():
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return client.get_collection(config.CHROMA_COLLECTION)


# =====================================================================
# 1) RETRIEVER - find the chunks whose meaning is closest to the question
# =====================================================================
def retrieve(question, k=config.TOP_K):
    question_vector = llm.embed([config.QUERY_PREFIX + question])[0]      # question -> vector
    result = _collection().query(query_embeddings=[question_vector], n_results=k)

    chunks = []
    for text, meta, distance in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        chunks.append({"text": text, "city": meta["city"], "page": meta["page"],
                       "score": round(1 - distance, 3)})                 # cosine similarity
    return chunks


# =====================================================================
# 2) AUGMENTATION - put the retrieved chunks into the prompt
# =====================================================================
PROMPT_TEMPLATE = """Answer the question using only the travel guide text below.
Answer in one or two short sentences.

Travel guide text:
{context}

Question: {question}
Answer:"""


def augment(question, chunks):
    context = "\n\n".join(chunk["text"] for chunk in chunks)
    return PROMPT_TEMPLATE.format(context=context, question=question)


# =====================================================================
# 3) GENERATION - the LLM writes the answer from the augmented prompt
# =====================================================================
def generate(prompt):
    return llm.chat(prompt)


def answer(question):
    """Run the full RAG pipeline and return everything the UI wants to show."""
    chunks = retrieve(question)
    prompt = augment(question, chunks)
    return {"answer": generate(prompt), "chunks": chunks, "prompt": prompt}
