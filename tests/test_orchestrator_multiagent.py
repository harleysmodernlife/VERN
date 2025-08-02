"""
Tests for VERN Orchestrator multi-cluster delegation and plugin/tool API calls.
"""

import unittest
from mvp.orchestrator import orchestrator_respond

class TestOrchestratorMultiAgent(unittest.TestCase):
    def test_multi_cluster_delegation(self):
        # Input that should trigger multiple clusters (e.g., research, finance, weather plugin)
        user_input = "What's the weather and my budget for this weekend's trip?"
        context = "Planning a trip for the weekend."
        agent_status = "All agents online"
        response = orchestrator_respond(user_input, context, agent_status)
        # Should include Phoenix synthesis and at least one cluster and one plugin/tool
        self.assertIn("[Phoenix Synthesis]:", response)
        self.assertTrue(any(tag in response for tag in ["[Research]:", "[Finance]:", "[Weather MCP Tool]:"]))
    
    def test_plugin_tool_api_call(self):
        # Input that should trigger a plugin/tool API call (e.g., calendar)
        user_input = "Schedule a meeting for tomorrow at 3pm."
        context = "User wants to schedule a meeting."
        agent_status = "All agents online"
        response = orchestrator_respond(user_input, context, agent_status)
        self.assertIn("[Calendar MCP Tool]:", response)

if __name__ == "__main__":
    unittest.main()
