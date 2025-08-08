import pytest
from vern_backend.app.memory import MemoryGraph
from vern_backend.app.vector_memory import VectorMemory, NoOpVectorMemory
from vern_backend.app.rag import NoOpRAGMemory

def test_memory_rag_retrieve():
    mem = MemoryGraph()
    mem.add_entity("doc1", {"text": "VERN supports RAG and semantic search"})
    mem.add_entity("doc2", {"text": "Long-term memory logging"})
    results = mem.rag_retrieve("semantic", top_k=2)
    assert "doc1" in results["entities"]

def test_vector_memory_rag_retrieve():
    vec_mem = NoOpVectorMemory()
    docs = ["VERN enables retrieval-augmented generation", "Semantic search is powerful"]
    vec_mem.add_documents(docs)
    results = vec_mem.rag_retrieve("semantic", top_k=2)
    assert isinstance(results, list)
    assert len(results) == 2
    assert results == docs[:2]

def test_rag_memory_noop_query():
    rag_mem = NoOpRAGMemory()
    docs = ["Doc A", "Doc B", "Doc C"]
    rag_mem.add_documents(docs)
    results = rag_mem.query("irrelevant", top_k=2)
    assert isinstance(results, list)
    assert len(results) == 2
    assert [r["content"] for r in results] == docs[:2]

def test_memory_logging():
    mem = MemoryGraph()
    mem.add_log({"event": "test", "value": 42})
    logs = mem.get_logs("test")
    assert any("test" in str(log) for log in logs)

def test_vector_memory_logging():
    vec_mem = NoOpVectorMemory()
    vec_mem.add_log({"event": "test", "value": 99})
    logs = vec_mem.get_logs("test")
    assert any("test" in str(log) for log in logs)

# TODO: Add integration tests for agent workflows using RAG and semantic memory.