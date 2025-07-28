"""
VERN Legal/Compliance Agent (LLM-Powered)
-----------------------------------------
Handles policy tracking, compliance, and legal questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def legal_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer legal/compliance questions, track policies, and suggest compliance actions.
    """
    prompt = (
        "You are the Legal/Compliance Agent in the VERN system. "
        "Your job is to answer legal and compliance questions, track policies, and help the user stay compliant. "
        "Use your knowledge and the provided context to give clear, responsible, and actionable advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Legal Agent:"
    )
    return call_qwen3(prompt)
