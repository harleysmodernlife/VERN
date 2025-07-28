"""
VERN Health/Wellness Agent (LLM-Powered)
----------------------------------------
Handles health, wellness, and habit tracking questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def health_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer health/wellness questions, suggest habits, and track wellness.
    """
    prompt = (
        "You are the Health/Wellness Agent in the VERN system. "
        "Your job is to answer health and wellness questions, suggest habits, and help the user track their well-being. "
        "Use your knowledge and the provided context to give safe, actionable, and supportive advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Health Agent:"
    )
    return call_qwen3(prompt)
