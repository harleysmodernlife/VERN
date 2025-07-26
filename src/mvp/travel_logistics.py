"""
Travel/Logistics Agent MVP

References:
- AGENT_GUIDES/TRAVEL_LOGISTICS.md
- AGENT_GUIDES/TRAVEL_LOGISTICS_PROMPTS.md
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'db')))
from logger import log_action, log_message

class TravelLogistics:
    def __init__(self, agent_id=15):
        self.agent_id = agent_id

    def handle_request(self, request, user_id=None):
        """
        Handle a travel/logistics request.
        """
        log_action(self.agent_id, user_id, "travel_logistics_request", {"request": request}, status="success")
        print(f"[TravelLogistics] Handling travel/logistics request: {request}")
        result = f"Travel/Logistics result for '{request}': [stubbed result]"
        self.log(result)
        return result

    def log(self, message):
        log_message(self.agent_id, message, level="info")
        print(f"[TravelLogistics] {message}")
