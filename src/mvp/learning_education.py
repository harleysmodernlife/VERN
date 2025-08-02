"""
VERN Learning/Education Agent (LLM-Powered)
-------------------------------------------
Handles personalized learning, skill mapping, and education questions using Ollama.
"""

from mvp.ollama_llm import call_ollama
from db.logger import log_action, log_message, log_gotcha

def learning_respond(user_input, context, agent_status=None, persona="default", user_id="default_user"):
    """
    Use Ollama to answer learning/education questions, suggest resources, and map skills.
    Logs all actions and errors for auditability. Supports persona/context adaptation and escalation stub.
    """
    agent_id = "learning_education"
    try:
        log_action(agent_id, user_id, "learning_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona
        }, status="started")

        prompt = (
            "You are the Learning/Education Agent in the VERN system. "
            "Your job is to help the user learn new skills, map their learning journey, and answer education-related questions. "
            "Use your knowledge and the provided context to give clear, supportive, and actionable advice. "
            "If you cannot answer directly, suggest which agent or tool to involve.\n\n"
            f"Context: {context}\n"
            f"Agent Status: {agent_status}\n"
            f"Persona: {persona}\n"
            f"User: {user_input}\n"
            "Learning Agent:"
        )
        response = call_ollama(prompt)
        log_action(agent_id, user_id, "llm_response", {
            "prompt": prompt,
            "response": str(response),
            "persona": persona
        })
        return response

    except Exception as e:
        log_message(agent_id, f"Error in learning_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona
        })
        log_gotcha(agent_id, f"Exception in learning_respond: {str(e)}", severity="error")
        from mvp.orchestrator import orchestrator_respond
        error_context = {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "error": str(e)
        }
        return orchestrator_respond(
            f"Learning Agent encountered an error: {str(e)}. Please escalate or suggest next steps.",
            error_context,
            agent_status,
            user_id
        )
