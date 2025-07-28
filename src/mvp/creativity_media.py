"""
VERN Creativity/Media Agent (LLM-Powered)
-----------------------------------------
Handles content creation, media management, and creative tasks using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def creativity_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer creativity/media questions, generate content, and manage media.
    """
    prompt = (
        "You are the Creativity/Media Agent in the VERN system. "
        "Your job is to help the user with content creation, media management, and creative tasks. "
        "Use your knowledge and the provided context to give imaginative, practical, and actionable advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Creativity Agent:"
    )
    return call_qwen3(prompt)
