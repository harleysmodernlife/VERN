"""
Automated test for cross-cluster handoff logging and DB validation.
Simulates a workflow: Dev Team → Admin → Knowledge Broker → Orchestrator.
"""

import sys
import os
import sqlite3

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from dev_team import DevTeam
from admin import Admin
from knowledge_broker import KnowledgeBroker
from orchestrator import Orchestrator

from logger import log_handoff

DB_PATH = "db/vern.db"

def fetch_latest(table, limit=1):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

def test_cross_cluster_handoff():
    dev_team = DevTeam()
    admin = Admin()
    knowledge_broker = KnowledgeBroker()
    orchestrator = Orchestrator(dev_team, admin)

    # Simulate a feature request workflow with explicit handoffs
    feature = "cross-cluster analytics"
    dev_result = dev_team.implement_feature(feature)
    log_handoff(dev_team.agent_id, admin.agent_id, 1, notes="Dev Team passes feature to Admin")
    admin_result = admin.schedule_meeting("handoff review for analytics")
    log_handoff(admin.agent_id, knowledge_broker.agent_id, 2, notes="Admin passes to Knowledge Broker")
    kb_result = knowledge_broker.context_lookup("handoff chain for analytics")
    log_handoff(knowledge_broker.agent_id, orchestrator.agent_id, 3, notes="Knowledge Broker passes to Orchestrator")

    # Validate handoffs in DB
    handoffs = fetch_latest("handoffs", limit=3)
    assert len(handoffs) >= 3, "Not enough handoffs logged"
    assert "Dev Team passes feature to Admin" in handoffs[2][5], "Dev→Admin handoff missing"
    assert "Admin passes to Knowledge Broker" in handoffs[1][5], "Admin→KB handoff missing"
    assert "Knowledge Broker passes to Orchestrator" in handoffs[0][5], "KB→Orchestrator handoff missing"
    print("Cross-cluster handoff logging: PASS")

def run_tests():
    print("Running cross-cluster handoff test...")
    test_cross_cluster_handoff()
    print("All cross-cluster handoff tests passed.")

if __name__ == "__main__":
    run_tests()
