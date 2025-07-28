"""
VERN Finance/Resource Agent (LLM-Powered)
-----------------------------------------
Handles budgeting, resource allocation, and finance questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def finance_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer finance/resource questions, budgeting, and resource allocation.
    """
    prompt = (
        "You are the Finance/Resource Agent in the VERN system. "
        "Your job is to answer finance and resource questions, help with budgeting, and manage resource allocation for the user. "
        "Use your knowledge and the provided context to give clear, actionable, and responsible advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Finance Agent:"
    )
    return call_qwen3(prompt)
