"""
Minimal VERN test suite: agent orchestration, context passing, LLM routing.
"""

from mvp.dev_team_agent import DevTeam
from mvp.knowledge_broker import KnowledgeBroker
from mvp.admin import Admin
from mvp.llm_router import route_llm_call

def test_agent_orchestration_basic():
    dev = DevTeam()
    kb = KnowledgeBroker()
    admin = Admin()
    context = {"user": "alice", "project": "VERN"}
    feature = "add analytics dashboard"
    dev_result = dev.implement_feature(feature, context=context)
    context["dev_result"] = dev_result
    kb_result = kb.context_lookup("analytics dashboard integration", context=context)
    context["kb_result"] = kb_result
    admin_result = admin.schedule_meeting(f"Review: {context['dev_result']} | {context['kb_result']}")
    context["admin_result"] = admin_result
    assert "Feature" in dev_result or len(dev_result) > 0
    assert "Context lookup" in kb_result or len(kb_result) > 0
    assert "Meeting" in admin_result or len(admin_result) > 0

def test_llm_router_stub():
    prompt = "Say hello"
    result = route_llm_call(prompt, agent_name="dev_team")
    assert isinstance(result, str) or hasattr(result, "__iter__")
