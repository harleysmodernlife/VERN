"""
VERN id10t Monitor Agent (LLM-Powered)
--------------------------------------
Sanity-checks actions for policy, stack, and convention adherence using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def id10t_monitor_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to sanity-check actions for policy, stack, and convention adherence.
    """
    prompt = (
        "You are the id10t Monitor Agent in the VERN system. "
        "Your job is to sanity-check actions, plans, and outputs for policy, stack, and convention adherence. "
        "Use your knowledge and the provided context to flag potential issues, suggest corrections, or escalate as needed. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "id10t Monitor Agent:"
    )
    return call_qwen3(prompt)
