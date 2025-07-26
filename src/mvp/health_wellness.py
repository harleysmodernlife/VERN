"""
Health/Wellness Agent MVP

References:
- AGENT_GUIDES/HEALTH_WELLNESS.md
- AGENT_GUIDES/HEALTH_WELLNESS_PROMPTS.md
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'db')))
from logger import log_action, log_message

class HealthWellness:
    def __init__(self, agent_id=8):
        self.agent_id = agent_id

    def handle_request(self, request, user_id=None):
        """
        Handle a health/wellness request.
        """
        log_action(self.agent_id, user_id, "health_wellness_request", {"request": request}, status="success")
        print(f"[HealthWellness] Handling health/wellness request: {request}")
        result = f"Health/Wellness result for '{request}': [stubbed result]"
        self.log(result)
        return result

    def log(self, message):
        log_message(self.agent_id, message, level="info")
        print(f"[HealthWellness] {message}")
