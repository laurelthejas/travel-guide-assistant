# 🧭 Travel Guide Assistant: RAG vs GraphRAG vs Agentic RAG

An app that answers questions about **10 city travel guides (PDF, 5 pages each)** in three different
ways, so you can compare them side by side. Everything runs **locally on a normal laptop CPU**: no cloud, no API keys.

| Approach | How it finds knowledge | Built with |
|---|---|---|
| 🔎 **RAG** | Splits the guides into chunks, embeds them, and fetches the chunks most similar to the question | ChromaDB |
| 🕸️ **GraphRAG** | Builds a knowledge graph (entities, relationships, communities) and answers from the graph | Microsoft GraphRAG |
| 🤖 **Agentic RAG** | An agent picks a search tool, grades the results, and retries with the other tool if they are not good enough | LangGraph |

The same three approaches are also available to other AI applications through an [MCP server](#mcp-server).

> 🪟 Built and tested on Windows 11, so the `.bat` launchers and setup commands below are for Windows; on macOS or Linux the Python code should work as is, started with `python llm_server.py` and then `streamlit run app.py`.

## Quick start

Double-click **`start_demo.bat`**. It:

1. checks that the setup is complete,
2. starts the local model server in its own minimised window (or reuses it if it is already running),
3. waits until the model server is ready,
4. starts the app, which opens at **http://localhost:8501** in your browser.

Double-clicking again while the app is running just opens it in the browser again.
**To stop:** close the app window and the "model server" window.

> 🛠️ The first time, do [Setup](#setup-first-time) and [Build the data](#build-the-data-one-time) first.

## What the app shows

| Tab | What you see |
|---|---|
| 📘 **Overview** | How each approach works (with diagrams) and the system status |
| 📄 **Documents** | Download and preview the 10 PDFs |
| 🔎 **RAG** | The answer, the retrieved chunks, the exact prompt sent to the model, and 👍/👎 feedback |
| 🕸️ **GraphRAG** | Local or global search, a picture of the knowledge-graph neighbourhood, the graph data used, and 👍/👎 |
| 🤖 **Agentic RAG** | The answer and a step-by-step trace of the agent's decisions, plus 👍/👎 |
| ⚖️ **Compare All** | One question, all three approaches side by side |
| ✅ **Evaluation** | Runs 13 "golden" questions through all three approaches, scores them, and summarises user feedback |
| 🔌 **MCP** | Connects to the app's MCP server, lists its tools, builds a form from each tool's input schema, and shows the result and the JSON-RPC request |

💡 Every question box has a **Sample questions** dropdown: pick one of 9 questions, or type your own as before. Each
sample was tested several times and answered correctly by all three approaches (GraphRAG with local search); they are
listed in `data/datasets/sample_questions.json`.

## The models

| Role | Model | Licence | Size |
|---|---|---|---|
| Answers (LLM) | [SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) | Apache 2.0 | ~138 MB |
| Embeddings | [BAAI bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) | MIT | ~35 MB |

Both run in [llama.cpp](https://github.com/ggml-org/llama.cpp) (via `llama-cpp-python`), which offers an
OpenAI-compatible API on `http://127.0.0.1:8000/v1`.

> The answer model is deliberately compact (135M parameters), so the whole system runs offline on a laptop CPU;
> expect short and sometimes wrong answers. The comparison therefore shows how much each retrieval approach adds. To use a bigger model, see [Using a bigger model](#using-a-bigger-model).

## Expected results

With the 135M-parameter model, the ✅ Evaluation tab gave (13 questions, October 2026):

| Approach | Average score | 👍 answers | Average time |
|---|---|---|---|
| 🕸️ GraphRAG | 0.56 | 9 of 13 | ~23 s |
| 🔎 RAG | 0.54 | 8 of 13 | ~2.5 s |
| 🤖 Agentic RAG | 0.50 | 8 of 13 | ~3.5 s |

GraphRAG was the only approach that scored on the "global" questions, the ones that need information from several
guides, but it is about 10 times slower. Most wrong answers come from the size of the answer model, not from the retrieval.

## MCP server

`mcp_server.py` makes the travel guides available to any [Model Context Protocol](https://modelcontextprotocol.io)
(MCP) client, such as an IDE or a desktop AI assistant. MCP is an open standard for connecting AI applications to
tools and data. The server offers five read-only tools:

| Tool | What it returns | Time in the 🔌 MCP tab |
|---|---|---|
| `list_guides` | The 10 cities and their PDF files | ~1 s |
| `search_guides` | The passages most similar to a query (the RAG retriever, without an LLM answer) | ~3 s |
| `ask_rag` | An answer from classic RAG, with the source pages | ~5 s |
| `ask_graphrag` | An answer from GraphRAG, with `local` or `global` search | ~50 s |
| `ask_agentic_rag` | An answer from the agent, with its step-by-step trace | ~35 s |

The times include starting the server, which takes about 25–30 s for the two tools that load Microsoft GraphRAG.

The client starts the server itself and talks to it over stdin/stdout (the stdio transport), so there is no need to
run it by hand: only the model server has to be running. To connect another MCP client, add a server entry like this,
with the path to your project folder:

```json
{
  "mcpServers": {
    "travel-guide-assistant": {
      "command": "C:\\path\\to\\travel-guide-assistant\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\travel-guide-assistant\\mcp_server.py"]
    }
  }
}
```

The file and key names differ between clients, so check your client's documentation. The 🔌 MCP tab shows this entry
with the paths of your own computer.

## Where to find each part in the code

| Part | File |
|---|---|
| RAG **Retriever / Augmentation / Generation** | `rag/basic_rag.py` (each part is marked with a `=====` banner) |
| GraphRAG search + a simple graph retriever | `rag/graph_rag.py` |
| Vector store used by GraphRAG | `rag/numpy_vector_store.py` (see [Design notes](#design-notes)) |
| Agent (route → retrieve → grade → switch_tool → generate) | `rag/agentic_rag.py` |
| Calls to the chat and embedding models | `rag/llm.py` |
| Golden-dataset scoring + 👍/👎 feedback | `rag/evaluation.py`, `data/datasets/golden_dataset.json`, `data/datasets/feedback.csv` |
| The app (8 tabs) | `app.py` |
| MCP server (5 tools) + the client used by the 🔌 MCP tab | `mcp_server.py`, `mcp_client.py` |
| All settings | `config.py` |
| Local model server (+ JSON adapter for GraphRAG) | `llm_server.py`, `llm_server_config.json` |

### Project map

```
travel-guide-assistant/
├── start_demo.bat            <- start everything (double-click)
├── start_llm_server.bat      <- start only the model server
├── run_app.bat               <- start only the app (model server must already run)
├── app.py, config.py, llm_server.py
├── mcp_server.py, mcp_client.py  <- MCP server + the app's MCP client
├── 1_generate_pdfs.py        <- step 1 of "Build the data"
├── 2_build_chroma.py         <- step 2
├── 3_build_graphrag.py       <- step 3
├── city_content.py           <- the text of the 10 travel guides
├── rag/                      <- the three approaches + evaluation
├── data/pdfs/                <- the 10 generated PDFs
├── data/datasets/            <- golden_dataset.json, sample_questions.json; feedback.csv + eval_results.csv (written by the app, not in git)
├── models/                   <- the two model files (not in git, ~173 MB)
├── chroma_db/                <- RAG index (built, not in git)
├── graphrag/                 <- GraphRAG settings + prompts; output/ is built, not in git
└── .streamlit/config.toml    <- app settings (no first-run email prompt, no usage statistics)
```

## Setup (first time)

On Windows, in PowerShell:

```powershell
winget install Python.Python.3.11
cd path\to\travel-guide-assistant  # the folder you cloned the project into
py -3.11 -m venv .venv            # or: & "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install "llama-cpp-python[server]==0.3.36" --only-binary=llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
# download the two models (~173 MB) into models/
.venv\Scripts\python.exe -c "from huggingface_hub import hf_hub_download as d; d('bartowski/SmolLM2-135M-Instruct-GGUF','SmolLM2-135M-Instruct-Q8_0.gguf',local_dir='models'); d('CompendiumLabs/bge-small-en-v1.5-gguf','bge-small-en-v1.5-q8_0.gguf',local_dir='models')"
```

## Build the data (one time)

1. Start the model server: double-click **`start_llm_server.bat`** and keep its window open.
2. Run these in order:

```powershell
.venv\Scripts\python.exe 1_generate_pdfs.py     # 10 PDFs -> data/pdfs/
.venv\Scripts\python.exe 2_build_chroma.py      # chunks + embeddings -> chroma_db/        (~1 min)
.venv\Scripts\python.exe 3_build_graphrag.py    # knowledge graph -> graphrag/output/     (~10-20 min)
```

If step 3 is interrupted, just run it again: finished parts are cached in `graphrag/cache/` and are reused.

## Using a bigger model

Answers get much better with a bigger model, for example **Llama 3.2 3B via [Ollama](https://ollama.com)** (~3 GB):

1. `ollama pull llama3.2:3b` and `ollama pull bge-m3`
2. In `config.py`, switch the three LLM settings to the Ollama block (it is already there, commented out).
3. Rebuild both indexes (`2_build_chroma.py` and `3_build_graphrag.py`), because the embedding model changed.
   With a bigger model you can also set `METHOD = "standard"` in `3_build_graphrag.py` (see the notes below).

## Troubleshooting

| Problem | What to do |
|---|---|
| The app says **"The LLM server is not running"** | Start it with `start_demo.bat` (or `start_llm_server.bat`), then refresh the page. |
| **"The model server did not answer within 2 minutes"** | Look at the "model server" window for the error. Often port 8000 is still used by an old server window: close it and try again. |
| A tab says the **index is not built** | Run the matching step in [Build the data](#build-the-data-one-time). |
| The 🔌 MCP tab says **"Could not start the MCP server"** | Install the packages again with `.venv\Scripts\python.exe -m pip install -r requirements.txt`: the `mcp` package was added later. |
| **"DLL load failed … An Application Control policy has blocked this file"** | Windows **Smart App Control** can block some compiled Python packages. It blocked LanceDB on the development PC, which is why GraphRAG uses the small `rag/numpy_vector_store.py` instead. Don't switch GraphRAG back to LanceDB. |
| Answers are **wrong or strange** | Expected with a 135M model. Check the retrieved chunks/graph data: if the right text was found, the retrieval worked and the model is the weak link. |
| The **first answer is slow** | The first requests can be slower while the models load. GraphRAG is always the slowest (~20–30 s per answer). |
| You see a **"Network URL"** when the app starts | The app can be opened from other devices on the same network. To keep it on your PC only, add `--server.address localhost` to the `streamlit` line in `start_demo.bat`. |

## License

MIT: see [LICENSE](LICENSE). The GraphRAG prompt and settings files come from Microsoft GraphRAG (also MIT); its
notice and the list of included files are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The models and Python
packages are downloaded during setup and keep their own licenses.

## Design notes

- **GraphRAG "fast" vs "standard":** with the 135M-parameter model we use `--method fast`. Entities and relationships are found
  with NLP (noun phrases that appear together), and the LLM only writes the community reports. With a bigger LLM, set
  `METHOD = "standard"` in `3_build_graphrag.py` so the LLM extracts the graph itself. A side effect of "fast": names
  can be split, for example "Statue of Liberty" becomes the entities STATUE and LIBERTY.
- **Agent decisions:** a big LLM would normally make the agent's *route* and *grade* decisions. Here they use simple
  rules and embedding similarity, because a 135M model can't decide reliably. The LangGraph loop is the same either way.
- **`llm_server.py`** contains a short adapter. GraphRAG requests JSON in the newer `json_schema` format, so the adapter
  converts that into llama.cpp's grammar-constrained `json_object`. As a result, even the 135M-parameter model always returns
  valid JSON.
- **GraphRAG's vector store:** GraphRAG normally stores its embeddings in LanceDB, which Smart App Control blocked on
  the development PC. `rag/numpy_vector_store.py` (about 100 lines) keeps the few hundred vectors in parquet files and searches
  them with cosine similarity. It is registered as vector store type `numpy` in `graphrag/settings.yaml`.
- **One MCP server process per call:** the 🔌 MCP tab starts `mcp_server.py` for every call and closes it afterwards.
  That keeps each call independent and the client code short, at the cost of the start-up time. A client that keeps
  the server running pays that cost only once.
- **Stdout in the MCP server:** with the stdio transport, stdout carries the protocol messages. The MCP library sends
  stray library output to stderr while it serves, and `mcp_server.py` does the same at exit, where LiteLLM (used by
  GraphRAG) prints a log line.

## 🔗 Related projects

- [📖🖋️ C-Caption Transformer](https://github.com/laurelthejas/c-caption-transformer): a decoder-only transformer built and trained from scratch that writes short C programs from English captions, with a plan and an explanation.
- [🎨 Diffusion Models: Image Generation and Captioning](https://github.com/laurelthejas/diffusion-models-image-generation-and-captioning): fine-tunes Stable Diffusion for text-to-image and image-to-image, and trains a text-to-image diffusion model from scratch on Fashion-MNIST.
- [🧩 Autoencoders: Feature Extraction, Colorization and Enhancement](https://github.com/laurelthejas/autoencoders-recognize-colorize-enhance): three image autoencoders trained from scratch on CIFAR-10, which recognize objects and find similar images, add color to grayscale images, and remove noise and blur.
