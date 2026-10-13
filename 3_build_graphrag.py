"""
Step 3 - Build the Microsoft GraphRAG knowledge graph.

  1. Convert each PDF into a .txt file in graphrag/input/
  2. `graphrag init`   -> creates settings.yaml + prompts/
  3. Point settings.yaml at our local LLM server and shrink token limits
     so they fit the small model's context window
  4. `graphrag index --method fast`
       "fast"     = entities/relationships found with NLP (noun phrases), LLM only writes summaries
       "standard" = the LLM extracts entities/relationships (needs a bigger model, e.g. Llama 3.2 3B)

Run (with the LLM server running):  .venv\\Scripts\\python.exe 3_build_graphrag.py
"""
import subprocess
import sys

import yaml
from pypdf import PdfReader

import config

ROOT = config.GRAPHRAG_ROOT
METHOD = "fast"          # change to "standard" when using a bigger LLM (see config.py)
SMALL = 3000             # token budget that fits a small model's context window

# `python -m graphrag`, but first register our "numpy" vector store
# (GraphRAG's default, LanceDB, has a DLL that Windows Smart App Control blocks)
CLI = "import rag.numpy_vector_store; from graphrag.cli.main import app; app(prog_name='graphrag')"


def graphrag(*args):
    subprocess.run([sys.executable, "-c", CLI, *args, "--root", str(ROOT)], check=True, cwd=config.ROOT)


def pdfs_to_text():
    (ROOT / "input").mkdir(parents=True, exist_ok=True)
    for pdf in sorted(config.PDF_DIR.glob("*.pdf")):
        pages = [page.extract_text() for page in PdfReader(pdf).pages]
        # drop the footer lines ("... educational demo content", "Page 1 of 5") so they don't become entities
        pages = ["\n".join(line for line in p.splitlines()
                           if "educational demo content" not in line and not line.startswith("Page "))
                 for p in pages]
        text = "\n\n".join(pages)
        (ROOT / "input" / f"{pdf.stem}.txt").write_text(text, encoding="utf-8")
        print("  wrote", pdf.stem + ".txt")


# GraphRAG's default report prompt is long and contains an example that tiny
# models copy word for word. This short travel-specific prompt works better.
# ({input_text} and {max_report_length} are filled in by GraphRAG.)
REPORT_PROMPT = """You write short reports about a group of related things (places, landmarks, food, transport, history) taken from city travel guides.

Using ONLY the text below, write a JSON report with:
- title: a short name for the group, including the city
- summary: one or two sentences about what connects these things
- findings: two key facts, each with a summary and an explanation
- rating: how important this is for a traveller, from 0 to 10
- rating_explanation: one sentence

Keep the report under {max_report_length} words.

Text:
{input_text}

JSON report:"""


def configure():
    (ROOT / "prompts" / "community_report_text.txt").write_text(REPORT_PROMPT, encoding="utf-8")

    settings_file = ROOT / "settings.yaml"
    s = yaml.safe_load(settings_file.read_text(encoding="utf-8"))

    # --- models: use our local OpenAI-compatible server (llama.cpp or Ollama)
    for section, model in [("completion_models", config.CHAT_MODEL), ("embedding_models", config.EMBED_MODEL)]:
        for model_cfg in s[section].values():
            model_cfg.update({"model_provider": "openai", "model": model,
                              "api_base": config.LLM_BASE_URL, "api_key": config.API_KEY})
    # cap answer length - small models otherwise may ramble until the context is full
    for model_cfg in s["completion_models"].values():
        model_cfg["call_args"] = {"max_tokens": 400}

    # --- keep every request small so indexing finishes in minutes on a laptop CPU
    s["concurrent_requests"] = 1
    s["vector_store"] = {"type": "numpy", "db_uri": "output/vectors"}   # see rag/numpy_vector_store.py
    s["cluster_graph"]["max_cluster_size"] = 25          # bigger clusters = fewer community reports to write
    s["chunking"].update({"size": 300, "overlap": 50})
    # entity types are only used by the "standard" (LLM) method
    s["extract_graph"].update({"max_gleanings": 0,
                               "entity_types": ["city", "landmark", "food", "transport", "person", "event"]})
    s["community_reports"].update({"max_length": 200, "max_input_length": 1200})
    s["local_search"].update({"max_context_tokens": SMALL, "top_k_entities": 5, "top_k_relationships": 5})
    s["global_search"] = {**s["global_search"], "max_context_tokens": SMALL, "data_max_tokens": SMALL,
                          "map_max_length": 300, "reduce_max_length": 300}
    s["basic_search"]["max_context_tokens"] = SMALL

    settings_file.write_text(yaml.safe_dump(s, sort_keys=False), encoding="utf-8")
    print("  settings.yaml configured for", config.CHAT_MODEL, "+", config.EMBED_MODEL)


if __name__ == "__main__":
    print("1) PDFs -> text"); pdfs_to_text()
    if not (ROOT / "settings.yaml").exists():
        print("2) graphrag init"); graphrag("init", "--model", config.CHAT_MODEL, "--embedding", config.EMBED_MODEL)
    print("3) configure"); configure()
    print(f"4) graphrag index --method {METHOD}  (this can take a while)"); graphrag("index", "--method", METHOD)
    print("Done. Knowledge graph saved in", ROOT / "output")
