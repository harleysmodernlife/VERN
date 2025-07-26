"""
Simple Message Bus MVP

Purpose:
- Facilitate communication between agents/clusters in the MVP.
- Pass a shared context dictionary for cross-agent workflows.
"""

class MessageBus:
    def __init__(self):
        self.handlers = {}

    def register(self, message_type, handler):
        """
        Register a handler for a specific message type.
        """
        self.handlers[message_type] = handler

    def send(self, message_type, payload, context=None):
        """
        Send a message to the appropriate handler, passing context if supported.
        """
        if message_type in self.handlers:
            handler = self.handlers[message_type]
            try:
                return handler(payload, context=context)
            except TypeError:
                # For backward compatibility with handlers that don't accept context
                return handler(payload)
        else:
            print(f"[MessageBus] No handler for message type: {message_type}")
            return None
