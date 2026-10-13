"""
app.py - Streamlit app: RAG vs GraphRAG vs Agentic RAG on 10 travel guides.

Run:  .venv\\Scripts\\streamlit.exe run app.py      (LLM server must be running)
"""
import json
import time

import pandas as pd
import streamlit as st
from pypdf import PdfReader

import config
from rag import agentic_rag, basic_rag, evaluation, graph_rag, llm

st.set_page_config(page_title="Travel Guide Assistant", page_icon="🧭", layout="wide")
st.title("🧭 Travel Guide Assistant: RAG vs GraphRAG vs Agentic RAG")
st.caption(f"10 city travel guides (PDF) · LLM: `{config.CHAT_MODEL}` · Embeddings: `{config.EMBED_MODEL}` · "
           f"Vector DB: ChromaDB · Graph: Microsoft GraphRAG · Agent: LangGraph")

if not llm.server_is_up():
    st.error("The LLM server is not running. Double-click **start_llm_server.bat**, then refresh this page.")
    st.stop()


# ------------------------------------------------------------------ helpers
SAMPLE_QUESTIONS = [s["question"] for s in json.loads(config.SAMPLE_QUESTIONS.read_text(encoding="utf-8"))]
TYPE_OWN = "✏️ Type your own question below"


def ask_box(key, default):
    """A sample-question dropdown + a question box + button. Returns the question when the button is clicked.
    Picking a sample copies it into the box; the box can still be edited or typed into freely."""
    q_key, s_key = f"q_{key}", f"s_{key}"
    st.session_state.setdefault(q_key, default)

    def use_sample():
        if st.session_state[s_key] != TYPE_OWN:
            st.session_state[q_key] = st.session_state[s_key]

    st.selectbox("Sample questions", [TYPE_OWN, *SAMPLE_QUESTIONS], key=s_key, on_change=use_sample,
                 help="Each sample was tested several times and answered correctly by RAG, "
                      "GraphRAG (local search) and Agentic RAG.")
    question = st.text_input("Your question", key=q_key)
    return question if st.button("Ask", key=f"b_{key}", type="primary") else None


def feedback_box(approach, question, answer, key):
    """Thumbs up / down + optional comment, saved to feedback.csv."""
    rating = st.feedback("thumbs", key=f"fb_{key}")
    comment = st.text_input("Comment (optional)", key=f"fc_{key}")
    if st.button("Send feedback", key=f"fs_{key}", disabled=rating is None):
        evaluation.save_feedback(approach, question, answer, "👍" if rating == 1 else "👎", comment)
        st.toast("Thanks! Feedback saved.")


def timed(fn, *args):
    start = time.time()
    try:
        result = fn(*args)
    except Exception as err:
        result = {"answer": f"⚠️ Error: {err}"}
    return result, round(time.time() - start, 1)


GRAPH_MISSING = "GraphRAG index not built yet. Run `.venv\\Scripts\\python.exe 3_build_graphrag.py` first."

tabs = st.tabs(["📘 Overview", "📄 Documents", "🔎 RAG", "🕸️ GraphRAG", "🤖 Agentic RAG",
                "⚖️ Compare All", "✅ Evaluation"])

# ================================================================== OVERVIEW
with tabs[0]:
    st.subheader("Three ways to give an LLM the right knowledge")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🔎 RAG\nSplit documents into **chunks**, store their **embeddings** in a vector "
                    "database (ChromaDB), and fetch the chunks most similar to the question.\n\n"
                    "✅ Simple, great for direct facts\n\n❌ Misses links spread across documents")
        st.graphviz_chart('digraph { rankdir=TB; node [shape=box, style=rounded];'
                          'Question -> "Retriever\\n(ChromaDB)" -> "Augmentation\\n(prompt + chunks)"'
                          ' -> "Generation\\n(LLM)" -> Answer }')
    with c2:
        st.markdown("### 🕸️ GraphRAG\nBuild a **knowledge graph** of entities and relationships "
                    "(Microsoft GraphRAG), group them into communities, and answer from the graph.\n\n"
                    "✅ Connects facts across documents\n\n❌ Expensive, slow indexing")
        st.graphviz_chart('digraph { rankdir=TB; node [shape=box, style=rounded];'
                          'Question -> "Retriever\\n(entities, relations,\\ncommunity reports)" -> '
                          '"Augmentation\\n(graph tables in prompt)" -> "Generation\\n(LLM)" -> Answer }')
    with c3:
        st.markdown("### 🤖 Agentic RAG\nAn **agent** (LangGraph) decides which tool to use, checks whether "
                    "the results are relevant, and retries with another tool if not.\n\n"
                    "✅ Flexible, self-correcting\n\n❌ More steps = more time")
        st.graphviz_chart(agentic_rag.AGENT_DOT)

    st.subheader("System status")
    s1, s2, s3 = st.columns(3)
    s1.metric("PDF documents", len(list(config.PDF_DIR.glob("*.pdf"))))
    try:
        s2.metric("Chunks in ChromaDB", basic_rag._collection().count())
    except Exception:
        s2.metric("Chunks in ChromaDB", "not built")
    if graph_rag.index_ready():
        s3.metric("Entities in knowledge graph", len(graph_rag.tables()["entities"]))
    else:
        s3.metric("Entities in knowledge graph", "not built")

# ================================================================== DOCUMENTS
with tabs[1]:
    st.subheader("The 10 travel guides (5 pages each)")
    pdfs = sorted(config.PDF_DIR.glob("*.pdf"))
    cols = st.columns(5)
    for i, pdf in enumerate(pdfs):
        cols[i % 5].download_button(f"⬇️ {pdf.stem.replace('_', ' ')}", pdf.read_bytes(),
                                    file_name=pdf.name, mime="application/pdf", key=f"dl_{pdf.name}")
    st.divider()
    chosen = st.selectbox("Preview a document", pdfs, format_func=lambda p: p.stem.replace("_", " "))
    page = st.radio("Page", [1, 2, 3, 4, 5], horizontal=True)
    st.text_area("Extracted text (this is what the retrievers see)",
                 PdfReader(chosen).pages[page - 1].extract_text(), height=300)

# ================================================================== RAG
with tabs[2]:
    st.subheader("🔎 Classic RAG with ChromaDB")
    question = ask_box("rag", "Who designed the Sydney Opera House?")
    if question:
        with st.spinner("Retrieving and generating..."):
            st.session_state.rag = (question, *timed(basic_rag.answer, question))
    if "rag" in st.session_state:
        q, result, secs = st.session_state.rag
        st.success(result["answer"])
        st.caption(f"⏱️ {secs} s")
        with st.expander("1️⃣ RETRIEVER — chunks found in ChromaDB", expanded=True):
            for c in result.get("chunks", []):
                st.markdown(f"**{c['city']} · page {c['page']} · similarity {c['score']}**")
                st.caption(c["text"])
        with st.expander("2️⃣ AUGMENTATION — the prompt sent to the LLM"):
            st.code(result.get("prompt", ""), language="text")
        st.markdown("3️⃣ **GENERATION** — the green box above is the LLM's answer.")
        feedback_box("RAG", q, result["answer"], "rag")

# ================================================================== GRAPHRAG
with tabs[3]:
    st.subheader("🕸️ Microsoft GraphRAG")
    if not graph_rag.index_ready():
        st.warning(GRAPH_MISSING)
    else:
        method = st.radio("Search method", ["local", "global"], horizontal=True,
                          help="local = start from entities in the question · global = use community summaries")
        if method == "global":
            st.caption("Global search reads only the community summaries, so it suits big-picture questions; "
                       "for specific facts like years or names, use local search.")
        question = ask_box("graph", "Which engineer worked on both the Statue of Liberty and a famous Paris landmark?")
        if question:
            with st.spinner(f"GraphRAG {method} search..."):
                st.session_state.graph = (question, *timed(graph_rag.answer, question, method))
        if "graph" in st.session_state:
            q, result, secs = st.session_state.graph
            st.success(result["answer"])
            st.caption(f"⏱️ {secs} s")
            entities = graph_rag.graph_retrieve(q)["entities"]
            if entities:
                with st.expander("🕸️ Knowledge-graph neighbourhood of the entities in your question", expanded=True):
                    st.graphviz_chart(graph_rag.subgraph_dot(entities))
            with st.expander("1️⃣ RETRIEVER + 2️⃣ AUGMENTATION — graph data GraphRAG put in the prompt"):
                for name, table in result.get("context", {}).items():
                    st.markdown(f"**{name}**")
                    st.dataframe(table, hide_index=True)
            feedback_box("GraphRAG", q, result["answer"], "graph")

        with st.expander("📊 Explore the whole knowledge graph"):
            t = graph_rag.tables()
            m1, m2, m3 = st.columns(3)
            m1.metric("Entities", len(t["entities"]))
            m2.metric("Relationships", len(t["relationships"]))
            m3.metric("Communities", len(t["communities"]))
            st.markdown("**Most connected entities**")
            st.dataframe(t["entities"].sort_values("degree", ascending=False)[["title", "degree", "frequency"]].head(20),
                         hide_index=True)

# ================================================================== AGENTIC RAG
with tabs[4]:
    st.subheader("🤖 Agentic RAG with LangGraph")
    st.graphviz_chart(agentic_rag.AGENT_DOT)
    question = ask_box("agent", "Which train connects London and Paris, and how long does the journey take?")
    if question:
        with st.spinner("The agent is working..."):
            st.session_state.agent = (question, *timed(agentic_rag.answer, question))
    if "agent" in st.session_state:
        q, result, secs = st.session_state.agent
        st.success(result["answer"])
        st.caption(f"⏱️ {secs} s")
        st.markdown("**Agent trace (what the agent decided, step by step):**")
        for step in result.get("steps", []):
            st.markdown(f"- {step}")
        feedback_box("Agentic RAG", q, result["answer"], "agent")

# ================================================================== COMPARE ALL
with tabs[5]:
    st.subheader("⚖️ Same question, three approaches")
    question = ask_box("cmp", "Which city did Emperor Constantine make the new Roman capital?")
    if question:
        runs = {}
        with st.spinner("Running RAG..."):
            runs["RAG"] = timed(basic_rag.answer, question)
        with st.spinner("Running GraphRAG..."):
            runs["GraphRAG"] = (timed(graph_rag.answer, question, "local") if graph_rag.index_ready()
                                else ({"answer": GRAPH_MISSING}, 0))
        with st.spinner("Running Agentic RAG..."):
            runs["Agentic RAG"] = timed(agentic_rag.answer, question)
        st.session_state.cmp = (question, runs)
    if "cmp" in st.session_state:
        q, runs = st.session_state.cmp
        for col, (name, (result, secs)) in zip(st.columns(3), runs.items()):
            with col:
                st.markdown(f"### {name}")
                st.info(result["answer"])
                st.caption(f"⏱️ {secs} s")
                feedback_box(name, q, result["answer"], f"cmp_{name}")

# ================================================================== EVALUATION
with tabs[6]:
    st.subheader("✅ Evaluation")
    st.markdown("**Golden dataset** — questions with known correct answers. An answer gets 👍 when it "
                f"contains at least {int(evaluation.PASS_SCORE * 100)}% of the expected keywords.")
    st.dataframe(pd.DataFrame(evaluation.load_golden()), hide_index=True)

    if st.button("▶️ Run Evaluation (all 3 approaches)", type="primary"):
        approaches = {"RAG": lambda q: basic_rag.answer(q)["answer"],
                      "Agentic RAG": lambda q: agentic_rag.answer(q)["answer"]}
        if graph_rag.index_ready():
            approaches["GraphRAG"] = lambda q: graph_rag.answer(q, "local")["answer"]
        bar = st.progress(0.0, text="Starting...")
        st.session_state.eval = evaluation.run_evaluation(approaches, lambda p, txt: bar.progress(p, text=txt))
        st.session_state.eval.to_csv(config.EVAL_RESULTS_FILE, index=False)
        bar.empty()

    if "eval" in st.session_state:
        df = st.session_state.eval
        summary = df.groupby("approach").agg(avg_score=("score", "mean"),
                                             thumbs_up=("verdict", lambda v: (v == "👍").sum()),
                                             questions=("verdict", "count"),
                                             avg_seconds=("seconds", "mean")).round(2)
        st.markdown("**Results by approach**")
        st.dataframe(summary)
        st.bar_chart(summary["avg_score"])
        st.markdown("**Score by question type**")
        st.dataframe(df.pivot_table(index="type", columns="approach", values="score", aggfunc="mean").round(2))
        st.markdown("**Every answer**")
        st.dataframe(df[["approach", "type", "question", "answer", "expected", "score", "verdict", "seconds"]],
                     hide_index=True)

    st.divider()
    st.subheader("👍👎 User feedback (from all tabs)")
    fb = evaluation.load_feedback()
    if fb.empty:
        st.info("No feedback yet — rate some answers in the other tabs.")
    else:
        counts = fb.pivot_table(index="approach", columns="rating", values="question", aggfunc="count", fill_value=0)
        st.dataframe(counts)
        st.markdown("**Latest feedback**")
        st.dataframe(fb.tail(10).iloc[::-1], hide_index=True)
