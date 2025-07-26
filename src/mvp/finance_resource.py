"""
Finance/Resource Agent MVP

References:
- AGENT_GUIDES/FINANCE_RESOURCE.md
- AGENT_GUIDES/FINANCE_RESOURCE_PROMPTS.md
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'db')))
from logger import log_action, log_message

class FinanceResource:
    def __init__(self, agent_id=7):
        self.agent_id = agent_id

    def handle_request(self, request, user_id=None):
        """
        Handle a finance/resource request.
        """
        log_action(self.agent_id, user_id, "finance_resource_request", {"request": request}, status="success")
        print(f"[FinanceResource] Handling finance/resource request: {request}")
        result = f"Finance/Resource result for '{request}': [stubbed result]"
        self.log(result)
        return result

    def log(self, message):
        log_message(self.agent_id, message, level="info")
        print(f"[FinanceResource] {message}")
