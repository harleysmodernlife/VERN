"""
VERN Career/Work Agent (LLM-Powered)
------------------------------------
Handles job search, networking, and performance questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def career_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer career/work questions, help with job search, networking, and performance.
    """
    prompt = (
        "You are the Career/Work Agent in the VERN system. "
        "Your job is to help the user with job search, networking, and performance improvement. "
        "Use your knowledge and the provided context to give practical, actionable, and supportive advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Career Agent:"
    )
    return call_qwen3(prompt)
