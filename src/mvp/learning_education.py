"""
VERN Learning/Education Agent (LLM-Powered)
-------------------------------------------
Handles personalized learning, skill mapping, and education questions using Qwen3.
"""

from src.mvp.qwen3_llm import call_qwen3

def learning_respond(user_input, context, agent_status=None):
    """
    Use Qwen3 to answer learning/education questions, suggest resources, and map skills.
    """
    prompt = (
        "You are the Learning/Education Agent in the VERN system. "
        "Your job is to help the user learn new skills, map their learning journey, and answer education-related questions. "
        "Use your knowledge and the provided context to give clear, supportive, and actionable advice. "
        "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Learning Agent:"
    )
    return call_qwen3(prompt)
