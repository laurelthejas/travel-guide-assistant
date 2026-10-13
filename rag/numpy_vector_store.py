"""
numpy_vector_store.py - a tiny vector store for GraphRAG (numpy + parquet files).

GraphRAG keeps its embeddings in LanceDB by default, but Windows Smart App
Control blocked LanceDB's compiled DLL on the development PC. A few hundred vectors don't
need a database anyway: this keeps each index in one parquet file and searches
it with plain cosine similarity.

Importing this module registers it as vector_store type "numpy" (see settings.yaml).
"""
from pathlib import Path

import numpy as np
import pandas as pd
from graphrag_vectors.vector_store import VectorStore, VectorStoreDocument, VectorStoreSearchResult
from graphrag_vectors.vector_store_factory import register_vector_store

import config


class NumpyVectorStore(VectorStore):
    def __init__(self, db_uri="output/vectors", **kwargs):
        super().__init__(**kwargs)
        folder = Path(db_uri) if Path(db_uri).is_absolute() else config.GRAPHRAG_ROOT / db_uri
        self.file = folder / f"{self.index_name}.parquet"
        self._set_rows(pd.DataFrame(columns=[self.id_field, self.vector_field,
                                             self.create_date_field, self.update_date_field]))

    def _set_rows(self, rows):
        self.rows = rows.reset_index(drop=True)
        # unit-length vectors, so a dot product = cosine similarity
        matrix = np.vstack(self.rows[self.vector_field]).astype(np.float32) if len(self.rows) else np.zeros((0, 0))
        norms = np.linalg.norm(matrix, axis=1, keepdims=True) if len(matrix) else 1
        self.matrix = matrix / np.where(norms == 0, 1, norms)

    def _save(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.rows.to_parquet(self.file)

    def _to_document(self, row, select=None, include_vectors=True):
        fields = select if select is not None else list(self.fields)
        return VectorStoreDocument(
            id=row[self.id_field],
            vector=list(row[self.vector_field]) if include_vectors else None,
            data={f: row[f] for f in fields if f in row},
            create_date=row[self.create_date_field],
            update_date=row[self.update_date_field])

    def connect(self):
        if self.file.exists():
            self._set_rows(pd.read_parquet(self.file))

    def create_index(self):
        self._set_rows(self.rows.iloc[0:0])
        self._save()

    def load_documents(self, documents):
        new = []
        for doc in documents:
            self._prepare_document(doc)
            if doc.vector is None:
                continue
            new.append({self.id_field: str(doc.id), self.vector_field: [float(x) for x in doc.vector],
                        self.create_date_field: doc.create_date, self.update_date_field: doc.update_date,
                        **{f: doc.data.get(f) for f in self.fields}})
        if new:
            self._set_rows(pd.concat([self.rows, pd.DataFrame(new)]) if len(self.rows) else pd.DataFrame(new))
            self._save()

    def similarity_search_by_vector(self, query_embedding, k=10, select=None, filters=None, include_vectors=True):
        if filters is not None:
            raise NotImplementedError("NumpyVectorStore does not support filters")
        if not len(self.rows):
            return []
        query = np.asarray(query_embedding, dtype=np.float32)
        scores = self.matrix @ (query / (np.linalg.norm(query) or 1))
        top = np.argsort(-scores)[:k]
        return [VectorStoreSearchResult(document=self._to_document(self.rows.iloc[i], select, include_vectors),
                                        score=float(scores[i]))
                for i in top]

    def search_by_id(self, id, select=None, include_vectors=True):
        match = self.rows[self.rows[self.id_field] == str(id)]
        if match.empty:
            raise IndexError(f"Document with id '{id}' not found.")
        return self._to_document(match.iloc[0], select, include_vectors)

    def count(self):
        return len(self.rows)

    def remove(self, ids):
        self._set_rows(self.rows[~self.rows[self.id_field].isin([str(i) for i in ids])])
        self._save()

    def update(self, document):
        self._prepare_update(document)
        rows = self.rows.copy()
        where = rows[self.id_field] == str(document.id)
        rows.loc[where, self.update_date_field] = document.update_date
        if document.vector is not None:
            rows.loc[where, self.vector_field] = pd.Series([list(document.vector)] * where.sum(),
                                                           index=rows.index[where])
        for f in self.fields:
            if f in (document.data or {}):
                rows.loc[where, f] = document.data[f]
        self._set_rows(rows)
        self._save()


register_vector_store("numpy", NumpyVectorStore)
