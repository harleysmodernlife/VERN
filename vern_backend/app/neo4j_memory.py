"""
VERN Neo4j Memory Subsystem (Scalable Knowledge Graph)

References:
- neo4j-labs/llm-graph-builder: https://github.com/neo4j-labs/llm-graph-builder
- Neo4j Python Driver: https://neo4j.com/docs/api/python-driver/current/

This module provides basic CRUD operations for entities and relationships using Neo4j.
"""

from neo4j import GraphDatabase
from typing import Dict, Any, List, Optional

class Neo4jMemory:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_entity(self, entity_id: str, properties: Dict[str, Any]):
        with self.driver.session() as session:
            session.run(
                "MERGE (e:Entity {id: $id}) SET e += $props",
                id=entity_id, props=properties
            )

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(
                "MATCH (e:Entity {id: $id}) RETURN e", id=entity_id
            )
            record = result.single()
            return dict(record["e"]) if record else None

    def add_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any] = {}):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Entity {id: $source}), (b:Entity {id: $target})
                MERGE (a)-[r:%s]->(b)
                SET r += $props
                """ % rel_type,
                source=source_id, target=target_id, props=properties
            )

    def get_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (a:Entity {id: $id})-[r]->(b:Entity)
                RETURN type(r) AS rel_type, b.id AS target, r AS properties
                """, id=entity_id
            )
            return [{"type": rec["rel_type"], "target": rec["target"], "properties": dict(rec["properties"])} for rec in result]

# Example usage:
# neo4j_mem = Neo4jMemory("bolt://localhost:7687", "neo4j", "password")
# neo4j_mem.add_entity("user_1", {"name": "Alice"})
# print(neo4j_mem.get_entity("user_1"))
# neo4j_mem.add_relationship("user_1", "project_42", "WORKS_ON")
# print(neo4j_mem.get_relationships("user_1"))
# neo4j_mem.close()
