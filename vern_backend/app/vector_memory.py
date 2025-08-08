"""
VERN Vector Memory Subsystem (Semantic Search)

References:
- txtai: https://github.com/neuml/txtai
- Haystack: https://github.com/deepset-ai/haystack

This module provides add/query functions for semantic memory using txtai.
"""

from txtai.embeddings import Embeddings
from typing import List, Dict, Any

class VectorMemory:
    def __init__(self, path: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embeddings = Embeddings({"path": path})

    def add_documents(self, docs: List[str], metadata: List[Dict[str, Any]] | None = None):
        # metadata is optional, can be used for filtering/search
        if metadata is None:
            metadata = [{} for _ in docs]
        self.embeddings.index([(str(i), doc, meta) for i, (doc, meta) in enumerate(zip(docs, metadata))])

    def query(self, text: str, top_k: int = 5):
        results = self.embeddings.search(text, top_k)
        return results

# Example usage:
# vector_memory = VectorMemory()
# vector_memory.add_documents(["Hello world", "VERN is modular"], [{"type": "greeting"}, {"type": "info"}])
# print(vector_memory.query("modular system"))
