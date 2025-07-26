"""
Research Agent MVP

References:
- AGENT_GUIDES/RESEARCH.md
- AGENT_GUIDES/RESEARCH_PROMPTS.md
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'db')))
from logger import log_action, log_message

from llm_router import call_llm_for_agent

class Research:
    def __init__(self, agent_id=6):
        self.agent_id = agent_id

    def handle_request(self, topic, user_id=None, context=None):
        """
        Handle a research request using LLM (stubbed).
        """
        log_action(self.agent_id, user_id, "research_request", {"topic": topic}, status="success")
        print(f"[Research] Handling research request: {topic}")
        llm_result = call_llm_for_agent("research", f"Research topic: {topic}", context)
        result = f"Research result for '{topic}': {llm_result}"
        self.log(result)
        return result

    def log(self, message):
        log_message(self.agent_id, message, level="info")
        print(f"[Research] {message}")
