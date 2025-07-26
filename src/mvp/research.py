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

class Research:
    def __init__(self, agent_id=6):
        self.agent_id = agent_id

    def handle_request(self, topic, user_id=None):
        """
        Handle a research request.
        """
        log_action(self.agent_id, user_id, "research_request", {"topic": topic}, status="success")
        print(f"[Research] Handling research request: {topic}")
        result = f"Research result for '{topic}': [stubbed result]"
        self.log(result)
        return result

    def log(self, message):
        log_message(self.agent_id, message, level="info")
        print(f"[Research] {message}")
