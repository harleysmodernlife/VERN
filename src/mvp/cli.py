"""
VERN CLI Chat (Streaming Orchestrator Output, Direct LLM Debug - PATCHED)
-------------------------------------------------------------------------
Interactive CLI for VERN with real-time streaming output from orchestrator, including context, DB, and multi-agent aggregation.
If orchestrator returns no response, fallback to direct LLM call for debugging.
(PATCHED: Avoid passing duplicate 'model' argument to route_llm_call)
"""

import sys
from mvp.llm_router import get_llm_backend, route_llm_call
from mvp.orchestrator import orchestrator_respond

def main():
    print("Welcome to VERN CLI Chat!")
    print("Type your message. Try natural language or commands like 'echo <text>', 'add <a> <b>', 'journal <entry>', 'schedule <details>', 'finance', 'profile <user_id>', 'last', or 'history'. Ctrl+C to exit.")
    chat_history = []
    user_id = "default_user"
    context = []
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting VERN CLI. Goodbye!")
                break
            context.append({"role": "user", "content": user_input})
            print("(orchestrator) Streaming orchestrator output:")
            response = orchestrator_respond(user_input, context=context, agent_status=None, user_id=user_id, verbose=True)
            # If orchestrator returns no response, fallback to direct LLM call for debugging
            if (isinstance(response, str) and ("Ollama error: No response received" in response or response.strip() == "")) or \
               (hasattr(response, "__iter__") and not isinstance(response, str) and not any(True for _ in response)):
                print("[DEBUG] Orchestrator returned no response. Fallback to direct LLM call:")
                provider, model = get_llm_backend()
                # PATCH: Only pass model if not already in kwargs
                direct_response = route_llm_call(user_input, stream=True)
                if hasattr(direct_response, "__iter__") and not isinstance(direct_response, str):
                    for chunk in direct_response:
                        print(chunk, end="", flush=True)
                    print()
                else:
                    print(direct_response)
            else:
                if hasattr(response, "__iter__") and not isinstance(response, str):
                    for chunk in response:
                        print(chunk, end="", flush=True)
                    print()
                    chat_history.append(("You", user_input))
                    chat_history.append(("VERN", "".join(list(response))))
                else:
                    print(response)
                    chat_history.append(("You", user_input))
                    chat_history.append(("VERN", response))
            context.append({"role": "vern", "content": response})
        except KeyboardInterrupt:
            print("\nExiting VERN CLI. Goodbye!")
            break

if __name__ == "__main__":
    main()
