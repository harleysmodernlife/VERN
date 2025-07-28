"""
VERN Archetype/Phoenix Agent (LLM-Powered)
------------------------------------------
Handles human reasoning, values, synthesis, and high-level guidance using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def archetype_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer high-level reasoning, values, synthesis, and guidance questions.
    """
    prompt = (
        "You are the Archetype/Phoenix Agent in the VERN system. "
        "Your job is to provide human reasoning, values alignment, synthesis, and high-level guidance for the user and other agents. "
        "Use your knowledge and the provided context to give wise, ethical, and holistic advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Archetype Agent:"
    )
    return call_qwen3(prompt)
