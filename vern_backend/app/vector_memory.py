"""
VERN Vector Memory Subsystem (Semantic Search)

References:
- txtai: https://github.com/neuml/txtai
- Haystack: https://github.com/deepset-ai/haystack

This module provides add/query functions for semantic memory using txtai.
"""
"""
VERN Vector Memory Subsystem (Semantic Search)
"""
# Supports RAG (retrieval-augmented generation), semantic search, and long-term logs.
# TODO: Integrate with external document stores for hybrid RAG.
# TODO: Add metadata-based filtering for semantic search.

# TODO: Ensure txtai is installed in the environment for semantic search.
try:
    from txtai.embeddings import Embeddings
    TXT_AI_AVAILABLE = True
except ImportError:
    Embeddings = None
    TXT_AI_AVAILABLE = False

import sqlite3
import os
from typing import List, Dict, Any, Optional

class VectorMemory:
    def __init__(self, path: str = "sentence-transformers/all-MiniLM-L6-v2", persistent: bool = False, db_path: str = "data/vector_memory.sqlite"):
        self.logs = []
        self.persistent = persistent
        self.db_path = db_path
        if TXT_AI_AVAILABLE:
            self.embeddings = Embeddings({"path": path})
        elif persistent:
            # Use SQLite for persistence if txtai is unavailable
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

    def add_documents(self, docs: List[str], metadata: List[Dict[str, Any]] | None = None):
        if metadata is None:
            metadata = [{} for _ in docs]
        if TXT_AI_AVAILABLE and self.embeddings:
            self.embeddings.index([(str(i), doc, meta) for i, (doc, meta) in enumerate(zip(docs, metadata))])
        elif self.persistent:
            for doc, meta in zip(docs, metadata):
                self.conn.execute(
                    "INSERT INTO documents (doc, meta) VALUES (?, ?)",
                    (doc, str(meta))
                )
            self.conn.commit()
        else:
            raise RuntimeError("Vector store unavailable: txtai not installed and persistence not enabled.")

    def query(self, text: str, top_k: int = 5):
        if TXT_AI_AVAILABLE and self.embeddings:
            results = self.embeddings.search(text, top_k)
            return results
        elif self.persistent:
            # Deterministic fallback: return top_k docs in insertion order
            cursor = self.conn.execute("SELECT doc FROM documents ORDER BY id ASC LIMIT ?", (top_k,))
            return [row[0] for row in cursor.fetchall()]
        else:
            raise RuntimeError("Vector store unavailable: txtai not installed and persistence not enabled.")

def rag_retrieve(self, query: str, top_k: int = 5):
    """
    RAG: Retrieve top_k relevant documents for a query.
    """
    try:
        results = self.query(query, top_k)
        return results
    except Exception as e:
        return {"error": f"RAG retrieval failed: {str(e)}"}

def add_log(self, log_entry: Dict[str, Any]) -> None:
    """
    Add a log entry to long-term semantic memory.
    """
    # TODO: Persist logs to external DB for durability.
    self.logs.append(log_entry)

def get_logs(self, filter_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve logs, optionally filtered by key.
    """
    if filter_key:
        return [log for log in self.logs if filter_key in str(log)]
    return self.logs

class NoOpVectorMemory:
    """
    Deterministic no-op vector store for tests.
    Always returns the first N docs for any query.
    """
    def __init__(self):
        self.docs = []
        self.logs = []

    def add_documents(self, docs: List[str], metadata: List[Dict[str, Any]] | None = None):
        self.docs = docs

    def query(self, text: str, top_k: int = 5):
        # Always return first top_k docs deterministically
        return self.docs[:top_k]

    def rag_retrieve(self, query: str, top_k: int = 5):
        return self.query(query, top_k)

    def add_log(self, log_entry: Dict[str, Any]) -> None:
        self.logs.append(log_entry)

    def get_logs(self, filter_key: Optional[str] = None) -> List[Dict[str, Any]]:
        if filter_key:
            return [log for log in self.logs if filter_key in str(log)]
        return self.logs

# Example usage:
# vector_memory = VectorMemory(persistent=True)
# vector_memory.add_documents(["Hello world", "VERN is modular"], [{"type": "greeting"}, {"type": "info"}])
# print(vector_memory.query("modular system"))
# no_op_vec = NoOpVectorMemory()
# no_op_vec.add_documents(["A", "B", "C"])
# print(no_op_vec.query("anything"))
