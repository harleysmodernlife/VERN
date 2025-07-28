"""
VERN Environment/Systems Agent (LLM-Powered)
--------------------------------------------
Handles device/system health, automation, and environment questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def environment_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer environment/systems questions, monitor device health, and suggest automations.
    """
    prompt = (
        "You are the Environment/Systems Agent in the VERN system. "
        "Your job is to monitor device and system health, suggest automations, and answer environment-related questions. "
        "Use your knowledge and the provided context to give practical, actionable, and safe advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Environment Agent:"
    )
    return call_qwen3(prompt)
