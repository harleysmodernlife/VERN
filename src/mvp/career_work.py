"""
Career/Work Agent MVP

References:
- AGENT_GUIDES/CAREER_WORK.md
- AGENT_GUIDES/CAREER_WORK_PROMPTS.md
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'db')))
from logger import log_action, log_message

class CareerWork:
    def __init__(self, agent_id=14):
        self.agent_id = agent_id

    def handle_request(self, request, user_id=None):
        """
        Handle a career/work request.
        """
        log_action(self.agent_id, user_id, "career_work_request", {"request": request}, status="success")
        print(f"[CareerWork] Handling career/work request: {request}")
        result = f"Career/Work result for '{request}': [stubbed result]"
        self.log(result)
        return result

    def log(self, message):
        log_message(self.agent_id, message, level="info")
        print(f"[CareerWork] {message}")
