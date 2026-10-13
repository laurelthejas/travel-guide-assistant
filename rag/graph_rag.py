"""
graph_rag.py - Microsoft GraphRAG.

Indexing (3_build_graphrag.py) turned the PDFs into a KNOWLEDGE GRAPH:
    entities (EIFFEL TOWER, GUSTAVE EIFFEL, ...) + relationships between them
    + communities (clusters of related entities) + community summary reports

At question time GraphRAG does Retrieval, Augmentation and Generation for us:
    LOCAL search  - starts from the entities in the question and follows their
                    relationships (good for specific / multi-hop questions)
    GLOBAL search - reads the community reports (good for "across all cities" questions)
"""
import asyncio
from functools import lru_cache

import pandas as pd
from graphrag_storage import create_storage
from graphrag_storage.tables.table_provider_factory import create_table_provider

import graphrag.api as api
from graphrag.config.load_config import load_config
from graphrag.data_model.data_reader import DataReader

import config
from rag import numpy_vector_store  # noqa: F401  registers the "numpy" vector store used in settings.yaml

RESPONSE_TYPE = "One or two short sentences"


def index_ready():
    """True once indexing has finished (community reports + embeddings are the last steps)."""
    out = config.GRAPHRAG_ROOT / "output"
    return (out / "community_reports.parquet").exists() and any((out / "vectors").glob("*.parquet"))


@lru_cache
def _load():
    """Load settings.yaml and the knowledge-graph tables produced by indexing."""
    gr_config = load_config(root_dir=config.GRAPHRAG_ROOT)
    reader = DataReader(create_table_provider(gr_config.table_provider,
                                              storage=create_storage(gr_config.output_storage)))
    tables = {name: asyncio.run(getattr(reader, name)())
              for name in ["entities", "relationships", "communities", "community_reports", "text_units"]}
    return gr_config, tables


def tables():
    return _load()[1]


# =====================================================================
# Full GraphRAG pipeline (Microsoft graphrag.api)
#   RETRIEVER    : GraphRAG finds matching entities, relationships,
#                  community reports and source text in the graph
#   AUGMENTATION : GraphRAG packs them into tables inside its prompt
#   GENERATION   : the LLM answers from that graph context
# =====================================================================
def answer(question, method="local"):
    gr_config, t = _load()
    if method == "global":
        response, context = asyncio.run(api.global_search(
            config=gr_config, entities=t["entities"], communities=t["communities"],
            community_reports=t["community_reports"], community_level=2,
            dynamic_community_selection=False, response_type=RESPONSE_TYPE, query=question))
    else:
        response, context = asyncio.run(api.local_search(
            config=gr_config, entities=t["entities"], communities=t["communities"],
            community_reports=t["community_reports"], text_units=t["text_units"],
            relationships=t["relationships"], covariates=None, community_level=2,
            response_type=RESPONSE_TYPE, query=question))
    # context = the retrieved graph data GraphRAG put in the prompt (dict of tables)
    context = {k: v for k, v in context.items() if isinstance(v, pd.DataFrame) and not v.empty}
    return {"answer": str(response).strip(), "context": context}


# =====================================================================
# Simple GRAPH RETRIEVER used by the Agentic RAG tool
#   1) find entities named in the question
#   2) follow their relationships to neighbouring entities
#   3) return the source text where those entities appear
# =====================================================================
def graph_retrieve(question, max_entities=4, max_relations=8, max_texts=3):
    t = tables()
    ents, rels, units = t["entities"], t["relationships"], t["text_units"]

    q = question.lower()
    matched = ents[ents["title"].str.lower().apply(lambda title: f" {title} " in f" {q} ")]
    matched = matched.sort_values("degree", ascending=False).head(max_entities)
    titles = list(matched["title"])

    related = rels[rels["source"].isin(titles) | rels["target"].isin(titles)]
    related = related.sort_values("weight", ascending=False).head(max_relations)

    # source text: text units that mention the most matched entities
    unit_ids = pd.Series([uid for ids in matched["text_unit_ids"] for uid in ids]).value_counts()
    texts = list(units.set_index("id").loc[unit_ids.index[:max_texts], "text"]) if len(unit_ids) else []

    facts = [f"{r.source} -- related to -- {r.target}" for r in related.itertuples()]
    context = ("Graph facts:\n" + "\n".join(facts) + "\n\nSource text:\n" + "\n\n".join(texts)) if titles else ""
    return {"entities": titles, "relationships": related[["source", "target", "weight"]], "texts": texts,
            "context": context}


def subgraph_dot(entity_titles, max_edges=25):
    """Graphviz picture of the entities and their direct neighbours."""
    rels = tables()["relationships"]
    edges = rels[rels["source"].isin(entity_titles) | rels["target"].isin(entity_titles)]
    edges = edges.sort_values("weight", ascending=False).head(max_edges)
    lines = ['graph G { rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#eef3ff", fontsize=10];']
    lines += [f'"{t}" [fillcolor="#ffd966"];' for t in entity_titles]
    lines += [f'"{e.source}" -- "{e.target}";' for e in edges.itertuples()]
    return "\n".join(lines + ["}"])
