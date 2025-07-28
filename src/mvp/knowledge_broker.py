"""
VERN Knowledge Broker Agent (LLM-Powered)
----------------------------------------
Checks memory/logs for existing answers before user queries, and helps escalate context.
"""

from src.mvp.qwen3_llm import call_qwen3

def knowledge_broker_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to check memory/logs for existing answers, escalate context, and suggest next steps.
    """
    prompt = (
        "You are the Knowledge Broker Agent in the VERN system. "
        "Your job is to check memory and logs for existing answers before user queries, and help escalate context to the right agent or cluster. "
        "Use your knowledge and the provided context to suggest answers, escalate as needed, or recommend next steps. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Knowledge Broker Agent:"
    )
    return call_qwen3(prompt)
