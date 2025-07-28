"""
VERN Orchestrator Agent (LLM-Powered)
-------------------------------------
Routes tasks, coordinates agents, and uses Qwen3 for reasoning.
"""

from src.mvp.qwen3_llm import call_qwen3

def orchestrator_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to decide which agent(s) should handle the user's request,
    and generate a summary plan.
    """
    prompt = (
        "You are the Orchestrator Agent in the VERN system. "
        "Your job is to read the user's message, consider the current context and agent status, "
        "and decide which agent clusters (Admin, Research, Finance, Health/Wellness, etc.) should handle the request. "
        "Summarize your reasoning and output a plan of action, including which agents to involve and why.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Orchestrator:"
    )
    return call_qwen3(prompt)
