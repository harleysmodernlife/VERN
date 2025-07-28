"""
VERN Security/Privacy Agent (LLM-Powered)
-----------------------------------------
Handles threat monitoring, audits, and privacy/security questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def security_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer security/privacy questions, monitor threats, and suggest audits.
    """
    prompt = (
        "You are the Security/Privacy Agent in the VERN system. "
        "Your job is to monitor threats, perform audits, and answer privacy/security questions for the user. "
        "Use your knowledge and the provided context to give safe, responsible, and actionable advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Security Agent:"
    )
    return call_qwen3(prompt)
