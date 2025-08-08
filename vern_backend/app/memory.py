"""
VERN Memory Subsystem: Knowledge Graph API

References:
- OpenSPG/KAG: https://github.com/OpenSPG/KAG
- neo4j-labs/llm-graph-builder: https://github.com/neo4j-labs/llm-graph-builder
- topoteretes/cognee: https://github.com/topoteretes/cognee

This module provides CRUD operations for entities, relationships, and temporal events in the agent memory graph.
"""

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
