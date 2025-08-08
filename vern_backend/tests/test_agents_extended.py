"""
Test: Agent Memory Subsystems (Knowledge Graph, Vector DB, Neo4j)

Validates CRUD operations and semantic search for all memory layers.
"""

from vern_backend.app.memory import MemoryGraph
from vern_backend.app.vector_memory import VectorMemory
from vern_backend.app.neo4j_memory import Neo4jMemory

def test_memory_graph_crud():
    mem = MemoryGraph()
    mem.add_entity("user_1", {"name": "Alice"})
    assert mem.get_entity("user_1")["name"] == "Alice"
    mem.add_event("user_1", "login", properties={"ip": "127.0.0.1"})
    events = mem.get_events("user_1")
    assert any(e["type"] == "login" for e in events)

def test_vector_memory_search():
    vm = VectorMemory()
    docs = ["Agents collaborate", "VERN is modular"]
    vm.add_documents(docs)
    results = vm.query("collaborate", top_k=2)
    assert len(results) > 0

import socket
import pytest

def _port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

@pytest.mark.skipif(not _port_open("localhost", 7687), reason="Neo4j not running on localhost:7687")
def test_neo4j_memory_crud():
    # Requires running Neo4j server at bolt://localhost:7687
    neo = Neo4jMemory("bolt://localhost:7687", "neo4j", "password")
    neo.add_entity("user_2", {"name": "Bob"})
    entity = neo.get_entity("user_2")
    assert entity and entity["name"] == "Bob"
    neo.add_relationship("user_2", "project_99", "WORKS_ON")
    rels = neo.get_relationships("user_2")
    assert any(r["type"] == "WORKS_ON" for r in rels)
    neo.close()
