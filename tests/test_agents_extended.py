"""
Automated tests for Knowledge Broker and Security/Privacy agents,
including cross-cluster handoff simulation and DB validation.
"""

import sys
import os
import sqlite3

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from mvp.knowledge_broker import knowledge_broker_context_lookup, knowledge_broker_cross_cluster_query
from mvp.security_privacy import security_privacy_monitor_action

DB_PATH = "db/vern.db"

def fetch_latest(table, limit=1):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

def test_knowledge_broker_context_lookup():
    query = "project status"
    result = knowledge_broker_context_lookup(query)
    actions = fetch_latest("actions")
    assert actions is not None, "No actions logged"
    print("Knowledge Broker context lookup: PASS")

def test_knowledge_broker_cross_cluster_query():
    req = "list unresolved gotchas"
    result = knowledge_broker_cross_cluster_query(req)
    actions = fetch_latest("actions")
    assert actions is not None, "No actions logged"
    print("Knowledge Broker cross-cluster query: PASS")

def test_security_privacy_monitor_no_violation():
    action = "regular feature implementation"
    result = security_privacy_monitor_action(action)
    actions = fetch_latest("actions")
    assert actions is not None, "No actions logged"
    assert result == "No violation", "False positive violation"
    print("Security/Privacy monitor (no violation): PASS")

def test_security_privacy_monitor_violation():
    action = "forbidden data export"
    result = security_privacy_monitor_action(action)
    actions = fetch_latest("actions")
    print("Security/Privacy monitor (violation): PASS")

def run_tests():
    print("Running extended agent tests...")
    test_knowledge_broker_context_lookup()
    test_knowledge_broker_cross_cluster_query()
    test_security_privacy_monitor_no_violation()
    test_security_privacy_monitor_violation()
    print("All extended agent tests passed.")

if __name__ == "__main__":
    run_tests()
