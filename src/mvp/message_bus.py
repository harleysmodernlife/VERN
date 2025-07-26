"""
Simple Message Bus MVP

Purpose:
- Facilitate communication between agents/clusters in the MVP.
"""

class MessageBus:
    def __init__(self):
        self.handlers = {}

    def register(self, message_type, handler):
        """
        Register a handler for a specific message type.
        """
        self.handlers[message_type] = handler

    def send(self, message_type, payload):
        """
        Send a message to the appropriate handler.
        """
        if message_type in self.handlers:
            return self.handlers[message_type](payload)
        else:
            print(f"[MessageBus] No handler for message type: {message_type}")
            return None
