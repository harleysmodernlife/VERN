"""
VERN RAG Subsystem (Haystack Integration)

References:
- Haystack: https://github.com/deepset-ai/haystack

Provides document ingestion and retrieval for agentic RAG workflows.
"""

from txtai.embeddings import Embeddings
from typing import List, Dict, Any

class RAGMemory:
    def __init__(self, path: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embeddings = Embeddings({"path": path})
        self.docs = []

    def add_documents(self, docs: List[str], meta: List[Dict[str, Any]] = None):
        if meta is None:
            meta = [{} for _ in docs]
        self.docs = docs
        self.embeddings.index([(str(i), doc, m) for i, (doc, m) in enumerate(zip(docs, meta))])

    def query(self, text: str, top_k: int = 5):
        results = self.embeddings.search(text, top_k)
        print("[RAG DEBUG] txtai search results:", results)
        out = []
        for r in results:
            # txtai returns (id, score)
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

# Example usage:
# rag = RAGMemory()
# rag.add_documents(["VERN supports RAG", "Agents use Haystack"], [{"type": "info"}, {"type": "tech"}])
# print(rag.query("RAG support"))
