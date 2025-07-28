"""
VERN Research Agent (LLM-Powered)
---------------------------------
Handles information retrieval, summarization, and research tasks using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def research_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer research/information requests, summarize, or suggest sources.
    """
    prompt = (
        "You are the Research Agent in the VERN system. "
        "Your job is to answer research questions, retrieve information, and summarize findings for the user. "
        "Use your knowledge and the provided context to give clear, concise, and actionable answers. "
        "If you cannot answer directly, suggest where to look or which agent to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Research Agent:"
    )
    return call_qwen3(prompt)
