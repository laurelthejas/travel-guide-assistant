"""
mcp_server.py - the Travel Guide Assistant as an MCP (Model Context Protocol) server.

MCP is an open standard that lets AI applications discover and call external tools. This server
offers the 10 travel guides and the three approaches as tools:

    list_guides       the 10 guides and their PDF files
    search_guides     the RAG retriever only: the chunks closest to a query, without an LLM answer
    ask_rag           classic RAG: retrieve chunks, then the LLM answers from them
    ask_graphrag      Microsoft GraphRAG, local or global search
    ask_agentic_rag   the LangGraph agent, with its step-by-step trace

An MCP client (the app's 🔌 MCP tab, an IDE or a desktop assistant) starts this script itself and
exchanges JSON-RPC messages with it over stdin/stdout (the "stdio" transport), so there is no need to
run it by hand. The local model server must be running (start_demo.bat or start_llm_server.bat).
"""
import os
import sys
import time
from typing import Annotated, Any, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

import config

server = MCPServer(
    name="travel-guide-assistant",
    instructions="Answers questions about 10 city travel guides (Barcelona, Dubai, Istanbul, London, New York, "
                 "Paris, Rome, Singapore, Sydney and Tokyo) with RAG, GraphRAG or Agentic RAG. "
                 "Use search_guides to see the source text, and the ask_* tools for a written answer.",
)

# The tools only read the guides and the local indexes; they change nothing.
READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)
Question = Annotated[str, Field(description="A question about one or more of the 10 cities.")]


def _check_ready(needs_graph=False):
    from rag import llm
    if not llm.server_is_up():
        raise ToolError("The local model server is not running. Start it with start_demo.bat or "
                        "start_llm_server.bat, then try again.")
    if not config.CHROMA_DIR.exists():
        raise ToolError("The RAG index is not built yet. Run 2_build_chroma.py first.")
    if needs_graph:
        from rag import graph_rag   # loads Microsoft GraphRAG, which takes a while
        if not graph_rag.index_ready():
            raise ToolError("The GraphRAG index is not built yet. Run 3_build_graphrag.py first.")


@server.tool(annotations=READ_ONLY)
def list_guides() -> list[dict[str, str]]:
    """List the 10 city travel guides (PDF, 5 pages each) that the other tools search."""
    return [{"city": pdf.stem.removesuffix("_Travel_Guide").replace("_", " "), "file": pdf.name}
            for pdf in sorted(config.PDF_DIR.glob("*.pdf"))]


@server.tool(annotations=READ_ONLY)
def search_guides(
    query: Annotated[str, Field(description="What to look for in the guides.")],
    k: Annotated[int, Field(ge=1, le=10, description="How many chunks to return.")] = config.TOP_K,
) -> list[dict[str, Any]]:
    """Find the guide passages most similar to the query (the RAG retriever, without an LLM answer).

    Each result has the city, the PDF page, the cosine similarity and the passage text."""
    _check_ready()
    from rag import basic_rag
    return basic_rag.retrieve(query, k)


@server.tool(annotations=READ_ONLY)
def ask_rag(question: Question) -> dict[str, Any]:
    """Answer with classic RAG: retrieve the closest chunks from ChromaDB, then the LLM answers from them.

    Fast (a few seconds) and best for specific facts. Returns the answer and the source pages."""
    _check_ready()
    from rag import basic_rag
    start = time.time()
    result = basic_rag.answer(question)
    return {"answer": result["answer"],
            "sources": [{"city": c["city"], "page": c["page"], "similarity": c["score"]} for c in result["chunks"]],
            "seconds": round(time.time() - start, 1)}


@server.tool(annotations=READ_ONLY)
def ask_graphrag(
    question: Question,
    method: Annotated[Literal["local", "global"], Field(
        description="local: start from the entities in the question (specific facts, multi-hop questions). "
                    "global: read the community summaries (big-picture questions across cities).")] = "local",
) -> dict[str, Any]:
    """Answer with Microsoft GraphRAG, which searches a knowledge graph of entities and relationships.

    Slower (about 20-30 seconds) but connects facts across guides. Returns the answer and how many rows
    of each graph table were used."""
    _check_ready(needs_graph=True)
    from rag import graph_rag
    start = time.time()
    result = graph_rag.answer(question, method)
    return {"answer": result["answer"], "method": method,
            "graph_rows_used": {name: len(table) for name, table in result["context"].items()},
            "seconds": round(time.time() - start, 1)}


@server.tool(annotations=READ_ONLY)
def ask_agentic_rag(question: Question) -> dict[str, Any]:
    """Answer with Agentic RAG: a LangGraph agent picks vector or graph search, grades the results,
    and retries with the other tool if they are not relevant enough.

    Returns the answer, the tool it ended with, and the agent's step-by-step trace."""
    _check_ready()
    from rag import agentic_rag
    start = time.time()
    result = agentic_rag.answer(question)
    return {"answer": result["answer"], "final_tool": result["tool"],
            "steps": [step.replace("**", "") for step in result["steps"]],
            "seconds": round(time.time() - start, 1)}


if __name__ == "__main__":
    server.run("stdio")   # while serving, stray prints go to stderr instead of the MCP messages
    # The transport hands stdout back when it stops; keep exit-time log lines (from LiteLLM) off it too.
    sys.stdout.flush()
    os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
