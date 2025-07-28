"""
VERN Admin Agent (LLM-Powered)
------------------------------
Handles scheduling, file management, and logistics using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def admin_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer admin/logistics questions, schedule events, and manage files.
    """
    prompt = (
        "You are the Admin Agent in the VERN system. "
        "Your job is to help with scheduling, file management, and logistics for the user. "
        "Use your knowledge and the provided context to give clear, organized, and actionable advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Admin Agent:"
    )
    return call_qwen3(prompt)
