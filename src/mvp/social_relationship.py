"""
VERN Social/Relationship Agent (LLM-Powered)
--------------------------------------------
Handles communication, event planning, and social questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def social_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer social/relationship questions, plan events, and help with communication.
    """
    prompt = (
        "You are the Social/Relationship Agent in the VERN system. "
        "Your job is to help the user with communication, event planning, and social/relationship questions. "
        "Use your knowledge and the provided context to give empathetic, practical, and actionable advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Social Agent:"
    )
    return call_qwen3(prompt)
