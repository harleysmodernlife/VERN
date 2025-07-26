"""
Automated tests for Knowledge Broker and Security/Privacy agents,
including cross-cluster handoff simulation and DB validation.
"""

import sys
import os
import sqlite3

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from knowledge_broker import KnowledgeBroker
from security_privacy import SecurityPrivacy
from dev_team import DevTeam
from admin import Admin

DB_PATH = "db/vern.db"

def fetch_latest(table, limit=1):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

def test_knowledge_broker_context_lookup():
    kb = KnowledgeBroker()
    query = "project status"
    result = kb.context_lookup(query)
    actions = fetch_latest("actions")
    assert actions, "No actions logged"
    assert query in actions[0][5], "Context lookup not logged"
    print("Knowledge Broker context lookup: PASS")

def test_knowledge_broker_cross_cluster_query():
    kb = KnowledgeBroker()
    req = "list unresolved gotchas"
    result = kb.cross_cluster_query(req)
    actions = fetch_latest("actions")
    assert actions, "No actions logged"
    assert req in actions[0][5], "Cross-cluster query not logged"
    print("Knowledge Broker cross-cluster query: PASS")

def test_security_privacy_monitor_no_violation():
    sp = SecurityPrivacy()
    action = "regular feature implementation"
    result = sp.monitor_action(action)
    actions = fetch_latest("actions")
    assert actions, "No actions logged"
    assert action in actions[0][5], "Security monitor action not logged"
    assert result == "No violation", "False positive violation"
    print("Security/Privacy monitor (no violation): PASS")

def test_security_privacy_monitor_violation():
    sp = SecurityPrivacy()
    action = "forbidden data export"
    result = sp.monitor_action(action)
    actions = fetch_latest("actions")
    gotchas = fetch_latest("gotchas")
    assert actions, "No actions logged"
    assert gotchas, "No gotchas logged"
    assert "forbidden" in actions[0][5], "Violation action not logged"
    assert "Policy violation" in gotchas[0][3], "Violation not logged as gotcha"
    assert result == "Violation flagged", "Violation not flagged"
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
