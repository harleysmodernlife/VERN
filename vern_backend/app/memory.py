"""
VERN Memory Subsystem: Knowledge Graph API

References:
- OpenSPG/KAG: https://github.com/OpenSPG/KAG
- neo4j-labs/llm-graph-builder: https://github.com/neo4j-labs/llm-graph-builder
- topoteretes/cognee: https://github.com/topoteretes/cognee

This module provides CRUD operations for entities, relationships, and temporal events in the agent memory graph.
"""
VERN Memory Subsystem: Knowledge Graph API

Supports RAG (retrieval-augmented generation), semantic search, and long-term logs.
"""
# TODO: Integrate with external document stores for hybrid RAG.
# TODO: Add advanced event/entity filtering for semantic search.

import os
from typing import Dict, Any, List, Optional
import datetime

import logging

class MemoryGraph:
    def __init__(self):
        # In-memory graph store (recommended default for resource-constrained setups)
        self.entities = {}
        self.relationships = []
        self.events = []
        self.logs = []  # Long-term logs for agent memory

    def add_entity(self, entity_id: str, properties: Dict[str, Any]) -> None:
        self.entities[entity_id] = properties

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        return self.entities.get(entity_id)

    def update_entity(self, entity_id: str, properties: Dict[str, Any]) -> None:
        if entity_id in self.entities:
            self.entities[entity_id].update(properties)

    def delete_entity(self, entity_id: str) -> None:
        if entity_id in self.entities:
            del self.entities[entity_id]

    def add_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any] = {}) -> None:
        self.relationships.append({
            "source": source_id,
            "target": target_id,
            "type": rel_type,
            "properties": properties
        })

    def get_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        return [rel for rel in self.relationships if rel["source"] == entity_id or rel["target"] == entity_id]

    def add_event(self, entity_id: str, event_type: str, timestamp: Optional[datetime.datetime] = None, properties: Dict[str, Any] = {}) -> None:
        self.events.append({
            "entity": entity_id,
            "type": event_type,
            "timestamp": timestamp or datetime.datetime.utcnow(),
            "properties": properties
        })

    def get_events(self, entity_id: str) -> List[Dict[str, Any]]:
        return [event for event in self.events if event["entity"] == entity_id]


    # RAG: Retrieve relevant entities/relationships/events for a query
    def rag_retrieve(self, query: str, top_k: int = 5) -> Dict[str, List[Any]]:
        """
        Semantic retrieval for RAG. Returns top_k relevant entities, relationships, and events.
        """
        # TODO: Replace with embedding-based similarity for production.
        # Simple keyword match (placeholder for semantic search)
        entities = [eid for eid, props in self.entities.items() if query.lower() in str(props).lower()]
        relationships = [rel for rel in self.relationships if query.lower() in str(rel).lower()]
        events = [evt for evt in self.events if query.lower() in str(evt).lower()]
        return {
            "entities": entities[:top_k],
            "relationships": relationships[:top_k],
            "events": events[:top_k]
        }

    # Long-term log storage
    def add_log(self, log_entry: Dict[str, Any]) -> None:
        """
        Add a log entry to long-term memory.
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

def get_memory_backend():
    """
    Selects the memory backend based on environment/config.
    Defaults to in-memory. Logs a warning if Neo4j is referenced but not available.
    """
    backend = os.getenv("VERN_MEMORY_BACKEND", "memory")
    if backend == "neo4j":
        try:
            from vern_backend.app.neo4j_memory import Neo4jMemory
            logging.warning("Neo4j backend selected. Ensure Neo4j is running and configured.")
            return Neo4jMemory(
                os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                os.getenv("NEO4J_USER", "neo4j"),
                os.getenv("NEO4J_PASSWORD", "password")
            )
        except ImportError:
            logging.error("Neo4j backend requested but neo4j driver not installed. Falling back to in-memory.")
    return MemoryGraph()

# Example usage:
# memory = MemoryGraph()
# memory.add_entity("user_1", {"name": "Alice", "role": "admin"})
# memory.add_relationship("user_1", "project_42", "works_on")
# memory.add_event("user_1", "login")
