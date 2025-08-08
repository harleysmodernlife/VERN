"""
VERN RAG Subsystem (Haystack Integration)

References:
- Haystack: https://github.com/deepset-ai/haystack

Provides document ingestion and retrieval for agentic RAG workflows.
"""

try:
    from txtai.embeddings import Embeddings
    TXT_AI_AVAILABLE = True
except ImportError:
    Embeddings = None
    TXT_AI_AVAILABLE = False

import sqlite3
import os
from typing import List, Dict, Any

class RAGMemory:
    def __init__(self, path: str = "sentence-transformers/all-MiniLM-L6-v2", persistent: bool = False, db_path: str = "data/rag_memory.sqlite"):
        self.docs = []
        self.persistent = persistent
        self.db_path = db_path
        if TXT_AI_AVAILABLE:
            self.embeddings = Embeddings({"path": path})
        elif persistent:
            self.embeddings = None
            self._init_sqlite()
        else:
            self.embeddings = None

    def _init_sqlite(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, doc TEXT, meta TEXT)"
        )
        self.conn.commit()

    def add_documents(self, docs: List[str], meta: List[Dict[str, Any]] = None):
        if meta is None:
            meta = [{} for _ in docs]
        self.docs = docs
        if TXT_AI_AVAILABLE and self.embeddings:
            self.embeddings.index([(str(i), doc, m) for i, (doc, m) in enumerate(zip(docs, meta))])
        elif self.persistent:
            for doc, m in zip(docs, meta):
                self.conn.execute(
                    "INSERT INTO documents (doc, meta) VALUES (?, ?)",
                    (doc, str(m))
                )
            self.conn.commit()
        else:
            raise RuntimeError("RAG vector store unavailable: txtai not installed and persistence not enabled.")

    def query(self, text: str, top_k: int = 5):
        if TXT_AI_AVAILABLE and self.embeddings:
            results = self.embeddings.search(text, top_k)
            print("[RAG DEBUG] txtai search results:", results)
            out = []
            for r in results:
                if isinstance(r, tuple) and len(r) == 2:
                    idx, score = r
                    try:
                        doc_text = self.docs[int(idx)]
                    except Exception:
                        doc_text = str(idx)
                    out.append({"content": doc_text, "score": score})
                elif isinstance(r, str):
                    out.append({"content": r, "score": None})
                elif isinstance(r, float):
                    out.append({"content": str(r), "score": r})
                else:
                    out.append({"content": str(r), "score": None})
            return out
        elif self.persistent:
            cursor = self.conn.execute("SELECT doc FROM documents ORDER BY id ASC LIMIT ?", (top_k,))
            return [{"content": row[0], "score": None} for row in cursor.fetchall()]
        else:
            raise RuntimeError("RAG vector store unavailable: txtai not installed and persistence not enabled.")

class NoOpRAGMemory:
    """
    Deterministic no-op RAG store for tests.
    Always returns the first N docs for any query.
    """
    def __init__(self):
        self.docs = []

    def add_documents(self, docs: List[str], meta: List[Dict[str, Any]] = None):
        self.docs = docs

    def query(self, text: str, top_k: int = 5):
        return [{"content": doc, "score": None} for doc in self.docs[:top_k]]

# Example usage:
# rag = RAGMemory(persistent=True)
# rag.add_documents(["VERN supports RAG", "Agents use Haystack"], [{"type": "info"}, {"type": "tech"}])
# print(rag.query("RAG support"))
# no_op_rag = NoOpRAGMemory()
# no_op_rag.add_documents(["A", "B", "C"])
# print(no_op_rag.query("anything"))
