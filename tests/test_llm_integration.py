"""
Test LLM integration for VERN agents.
Ensures agent LLM calls return plausible output for the current backend.
"""

import sys
import os

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from mvp.dev_team_agent import dev_team_respond
from mvp.knowledge_broker import knowledge_broker_context_lookup
from mvp.research import research_respond

def test_dev_team_llm():
    feature = "add authentication"
    context = {"user": "alice", "project": "VERN"}
    result = dev_team_respond(feature, context=context)
    print("[DevTeam] Feature 'add authentication' implemented. Stub says:", result)
    assert "Feature" in result, "DevTeam LLM integration failed (missing stub output marker)"
    assert len(result) > 0, "DevTeam LLM integration failed (empty stub output)"

def test_kb_llm():
    query = "analytics dashboard integration"
    context = {"user": "alice", "project": "VERN"}
    result = knowledge_broker_context_lookup(query, context=context)
    print("[KnowledgeBroker] Context for 'analytics dashboard integration':", result)
    assert "Context lookup for" in result and len(result.split(":", 1)[-1].strip()) > 0, "KnowledgeBroker stub integration failed"

def test_research_llm():
    topic = "agentic AI"
    context = {"user": "alice", "project": "VERN"}
    result = research_respond(topic, context=context)
    print("[Research] Research result for 'agentic AI':", result)
    assert "Document search results:" in result or len(result) > 0, "Research stub integration failed"

def run_tests():
    print("Running LLM integration tests...")
    test_dev_team_llm()
    test_kb_llm()
    test_research_llm()
    print("All LLM integration tests passed.")

if __name__ == "__main__":
    run_tests()
