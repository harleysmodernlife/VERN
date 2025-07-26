"""
Test LLM integration for VERN agents.
Ensures agent LLM calls return plausible output for the current backend.
"""

import sys
import os

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from dev_team import DevTeam
from knowledge_broker import KnowledgeBroker
from research import Research

def test_dev_team_llm():
    dev = DevTeam()
    feature = "add authentication"
    context = {"user": "alice", "project": "VERN"}
    result = dev.implement_feature(feature, context=context)
    print("[DevTeam] Feature 'add authentication' implemented. LLM says:", result)
    assert "LLM says:" in result, "DevTeam LLM integration failed (missing LLM output marker)"
    # Accept any non-empty LLM output for modular backends
    llm_output = result.split("LLM says:", 1)[-1].strip()
    assert len(llm_output) > 0, "DevTeam LLM integration failed (empty LLM output)"

def test_kb_llm():
    kb = KnowledgeBroker()
    query = "analytics dashboard integration"
    context = {"user": "alice", "project": "VERN"}
    result = kb.context_lookup(query, context=context)
    print("[KnowledgeBroker] Context for 'analytics dashboard integration':", result)
    assert "Context for" in result and len(result.split(":", 1)[-1].strip()) > 0, "KnowledgeBroker LLM integration failed"

def test_research_llm():
    research = Research()
    topic = "agentic AI"
    context = {"user": "alice", "project": "VERN"}
    result = research.handle_request(topic, context=context)
    print("[Research] Research result for 'agentic AI':", result)
    assert "Research result for" in result and len(result.split(":", 1)[-1].strip()) > 0, "Research LLM integration failed"

def run_tests():
    print("Running LLM integration tests...")
    test_dev_team_llm()
    test_kb_llm()
    test_research_llm()
    print("All LLM integration tests passed.")

if __name__ == "__main__":
    run_tests()
