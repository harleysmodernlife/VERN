"""
VERN CLI Chat Interface (Multi-Agent)
-------------------------------------
Handles user input, routes to Orchestrator, and displays multi-agent responses.
"""

import sys
from src.mvp.orchestrator import orchestrator_respond

def main():
    print("Welcome to VERN CLI Chat!")
    print("Type your message. Try natural language or commands like 'echo <text>', 'add <a> <b>', 'journal <entry>', 'schedule <details>', 'finance', 'profile <user_id>', 'last', or 'history'. Ctrl+C to exit.")
    context = []
    agent_status = "All agents online"
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            # Add user input to context
            context.append(f"You: {user_input}")
            # Call Orchestrator for response
            response = orchestrator_respond(user_input, "\n".join(context[-10:]), agent_status)
            print(f"(orchestrator) {response}")
            # Add orchestrator response to context
            context.append(f"Orchestrator: {response}")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting VERN CLI. Goodbye!")

if __name__ == "__main__":
    main()
