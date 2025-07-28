"""
VERN Emergent Agent (LLM-Powered)
---------------------------------
Scans for cross-cluster optimizations, creative solutions, and system-wide insights using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def emergent_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to find cross-cluster optimizations, creative solutions, and system-wide insights.
    """
    prompt = (
        "You are the Emergent Agent in the VERN system. "
        "Your job is to scan for cross-cluster optimizations, creative solutions, and system-wide insights. "
        "Use your knowledge and the provided context to suggest improvements, synergies, or new approaches. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Emergent Agent:"
    )
    return call_qwen3(prompt)
