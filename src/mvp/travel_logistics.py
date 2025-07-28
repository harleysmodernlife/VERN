"""
VERN Travel/Logistics Agent (LLM-Powered)
-----------------------------------------
Handles trip planning, navigation, and logistics questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def travel_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer travel/logistics questions, plan trips, and help with navigation.
    """
    prompt = (
        "You are the Travel/Logistics Agent in the VERN system. "
        "Your job is to help the user plan trips, navigate, and answer logistics-related questions. "
        "Use your knowledge and the provided context to give practical, actionable, and safe advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Travel Agent:"
    )
    return call_qwen3(prompt)
