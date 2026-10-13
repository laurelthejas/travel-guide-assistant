"""
agentic_rag.py - Agentic RAG with LangGraph.

Instead of one fixed pipeline, an AGENT decides what to do, checks its own
work and tries again if needed:

    route --> retrieve --> grade --(relevant)--> generate --> END
                 ^           |
                 |      (not relevant)
                 +--- switch_tool <--+     (at most one retry)

Tools the agent can use:
    "vector" - ChromaDB similarity search (classic RAG retriever)
    "graph"  - GraphRAG knowledge graph (entities + relationships)

Note for the class: with a big LLM, the route and grade decisions are usually
made by asking the LLM. Our tiny 135M model is not reliable enough for that,
so here they use simple rules + embedding similarity. The agent loop is the same.
"""
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

import config
from rag import basic_rag, graph_rag, llm

RELEVANCE_THRESHOLD = 0.6
GRAPH_WORDS = ["which cities", "connect", "link", "both", "compare", "between", "inspired",
               "partnership", "related", "relationship", "all cities", "same"]


class AgentState(TypedDict):
    question: str
    tool: str                                   # "vector" or "graph"
    context: str
    texts: list
    relevance: float
    attempts: int
    answer: str
    steps: Annotated[list, operator.add]        # each node ADDS lines to the trace


def cosine_relevance(question, texts):
    """Best cosine similarity between the question and the retrieved texts (0..1)."""
    if not texts:
        return 0.0
    vectors = llm.embed([config.QUERY_PREFIX + question] + list(texts))
    q, rest = vectors[0], vectors[1:]
    norm = lambda v: sum(x * x for x in v) ** 0.5
    return max(sum(a * b for a, b in zip(q, v)) / (norm(q) * norm(v)) for v in rest)


# ----------------------------------------------------------------- nodes
def route(state):
    """DECIDE which tool fits the question."""
    q = state["question"].lower()
    wants_graph = any(word in q for word in GRAPH_WORDS) and graph_rag.index_ready()
    tool = "graph" if wants_graph else "vector"
    reason = "question is about connections between things" if wants_graph else "question asks for a specific fact"
    return {"tool": tool, "attempts": 0, "steps": [f"🧭 Route: use **{tool}** search ({reason})"]}


# ===== RETRIEVER =====
def retrieve(state):
    if state["tool"] == "vector":
        chunks = basic_rag.retrieve(state["question"])
        texts = [c["text"] for c in chunks]
        found = ", ".join(f"{c['city']} p.{c['page']}" for c in chunks)
    else:
        result = graph_rag.graph_retrieve(state["question"])
        texts = result["texts"]
        found = ", ".join(result["entities"]) or "no matching entities"
    return {"texts": texts, "context": "\n\n".join(texts), "attempts": state["attempts"] + 1,
            "steps": [f"🔎 Retrieve with {state['tool']} search → {found}"]}


def grade(state):
    """CHECK: is what we found actually relevant to the question?"""
    score = cosine_relevance(state["question"], state["texts"])
    verdict = "relevant ✅" if score >= RELEVANCE_THRESHOLD else "not relevant enough ❌"
    return {"relevance": score, "steps": [f"🧪 Grade: similarity {score:.2f} → {verdict}"]}


def switch_tool(state):
    """RETRY: try the other tool."""
    other = "graph" if state["tool"] == "vector" and graph_rag.index_ready() else "vector"
    return {"tool": other, "steps": [f"🔁 Retry: switching to **{other}** search"]}


# ===== AUGMENTATION + GENERATION =====
def generate(state):
    prompt = basic_rag.augment(state["question"], [{"text": t} for t in state["texts"]])   # AUGMENTATION
    answer = llm.chat(prompt)                                                              # GENERATION
    return {"answer": answer, "steps": ["✍️ Generate: answer written from the retrieved context"]}


def after_grade(state):
    if state["relevance"] >= RELEVANCE_THRESHOLD or state["attempts"] >= 2:
        return "generate"
    return "switch_tool"


# ----------------------------------------------------------------- the graph
def build_agent():
    g = StateGraph(AgentState)
    g.add_node("route", route)
    g.add_node("retrieve", retrieve)
    g.add_node("grade", grade)
    g.add_node("switch_tool", switch_tool)
    g.add_node("generate", generate)

    g.set_entry_point("route")
    g.add_edge("route", "retrieve")
    g.add_edge("retrieve", "grade")
    g.add_conditional_edges("grade", after_grade, {"generate": "generate", "switch_tool": "switch_tool"})
    g.add_edge("switch_tool", "retrieve")
    g.add_edge("generate", END)
    return g.compile()


AGENT = build_agent()

AGENT_DOT = """digraph { rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#eef3ff"];
  route -> retrieve -> grade; grade -> generate [label="relevant"];
  grade -> switch_tool [label="not relevant"]; switch_tool -> retrieve; generate -> END; }"""


def answer(question):
    state = AGENT.invoke({"question": question, "steps": []})
    return {"answer": state["answer"], "steps": state["steps"], "tool": state["tool"]}
