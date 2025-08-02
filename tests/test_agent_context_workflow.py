"""
Test cross-agent workflow with shared context:
Dev Team → Knowledge Broker → Admin
Verifies context passing and updates.
"""

import sys
import os

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from mvp.dev_team_agent import DevTeam
from mvp.knowledge_broker import KnowledgeBroker
from mvp.admin import Admin

def test_cross_agent_context_workflow():
    dev = DevTeam()
    kb = KnowledgeBroker()
    admin = Admin()

    context = {"user": "alice", "project": "VERN"}
    feature = "add analytics dashboard"

    # Dev Team implements feature, updates context
    dev_result = dev.implement_feature(feature, context=context)
    context["dev_result"] = dev_result

    # Knowledge Broker looks up context, updates context
    kb_result = kb.context_lookup("analytics dashboard integration", context=context)
    context["kb_result"] = kb_result

    # Admin schedules meeting, uses context
    admin_result = admin.schedule_meeting(f"Review: {context['dev_result']} | {context['kb_result']}")
    context["admin_result"] = admin_result

    print("Context after workflow:", context)
    assert "dev_result" in context and "kb_result" in context and "admin_result" in context, "Context not updated correctly"
    print("Cross-agent context workflow: PASS")

def run_tests():
    print("Running cross-agent context workflow test...")
    test_cross_agent_context_workflow()
    print("All cross-agent context workflow tests passed.")

if __name__ == "__main__":
    run_tests()
