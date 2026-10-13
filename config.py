"""
config.py - ONE place for all settings.

The app talks to the LLM through an OpenAI-compatible API, so you can swap
the model just by changing the three LLM settings below.
"""
from pathlib import Path

# ---------------------------------------------------------------- LLM settings
# Default: tiny open-source models served locally by llama.cpp
#   (start it with start_llm_server.bat)
#   - SmolLM2-135M-Instruct  (HuggingFaceTB, Apache 2.0)  ~138 MB
#       model page: https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct
#       file used:  SmolLM2-135M-Instruct-Q8_0.gguf from https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF
#   - BAAI bge-small-en-v1.5 (MIT)                        ~35 MB
#       model page: https://huggingface.co/BAAI/bge-small-en-v1.5
#       file used:  bge-small-en-v1.5-q8_0.gguf from https://huggingface.co/CompendiumLabs/bge-small-en-v1.5-gguf
# The model files are NOT in git. Download both into the models/ folder (one time, ~173 MB):
#   .venv\Scripts\python.exe -c "from huggingface_hub import hf_hub_download as d; d('bartowski/SmolLM2-135M-Instruct-GGUF','SmolLM2-135M-Instruct-Q8_0.gguf',local_dir='models'); d('CompendiumLabs/bge-small-en-v1.5-gguf','bge-small-en-v1.5-q8_0.gguf',local_dir='models')"
# The file names and short names (aliases) the server uses are set in llm_server_config.json.
LLM_BASE_URL = "http://127.0.0.1:8000/v1"
CHAT_MODEL = "smollm2-135m"
EMBED_MODEL = "bge-small"

# Backup option: Ollama + Llama 3.2 3B (better answers, ~3 GB download)
#   install Ollama from https://ollama.com, then:
#   ollama pull llama3.2:3b  &&  ollama pull bge-m3
# LLM_BASE_URL = "http://localhost:11434/v1"
# CHAT_MODEL = "llama3.2:3b"
# EMBED_MODEL = "bge-m3"
# NOTE: if you change EMBED_MODEL, rebuild both indexes (steps 2 and 3).

API_KEY = "not-needed"  # local servers ignore the key, but the client needs one

# bge models search better when the QUESTION (not the documents) gets this prefix.
# Set to "" for other embedding models.
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# ---------------------------------------------------------------- Paths
ROOT = Path(__file__).parent
PDF_DIR = ROOT / "data" / "pdfs"
CHROMA_DIR = ROOT / "chroma_db"
CHROMA_COLLECTION = "travel_guides"
GRAPHRAG_ROOT = ROOT / "graphrag"
DATASET_DIR = ROOT / "data" / "datasets"
GOLDEN_DATASET = DATASET_DIR / "golden_dataset.json"   # questions with known answers (in git)
FEEDBACK_FILE = DATASET_DIR / "feedback.csv"           # thumbs up/down from the app (not in git)
EVAL_RESULTS_FILE = DATASET_DIR / "eval_results.csv"   # last Evaluation-tab run (not in git)
SAMPLE_QUESTIONS = DATASET_DIR / "sample_questions.json"  # dropdown questions, tested on all 3 approaches (in git)

# ---------------------------------------------------------------- RAG settings
CHUNK_SIZE = 800      # characters per chunk
CHUNK_OVERLAP = 150   # characters shared between neighbouring chunks
TOP_K = 3             # how many chunks the retriever returns
