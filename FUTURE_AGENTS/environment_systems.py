"""
VERN Environment & Systems Agent (Function-Based)
-------------------------------------------------
Handles sustainability, energy, and systems monitoring for the MVP.
"""

from src.db.logger import log_action, log_message, log_gotcha

def environment_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles environment/systems queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "environment"
    try:
        log_action(agent_id, user_id, "environment_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from src.mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Environment & Systems Agent. Advise on sustainability, energy, and systems monitoring.",
            "analyst": "You are an environmental analyst. Summarize trends, risks, and opportunities.",
            "advisor": "You are an environment advisor. Recommend actions and connect the user to relevant agents or plugins.",
            "monitor": "You are a systems monitor. Track metrics and alert the user to issues.",
            "engineer": "You are a systems engineer. Design and optimize sustainable solutions."
        }
        prompt = (
            persona_prompt.get(persona, persona_prompt["default"]) + "\n"
            f"Query: {user_input}\n"
            f"Context: {context}\n"
            f"Agent Status: {agent_status}\n"
            f"Persona: {persona}\n"
            f"Memory: {memory}\n"
        )
        response = route_llm_call(prompt, context=context, agent_status=agent_status)
        log_action(agent_id, user_id, "llm_response", {
            "prompt": prompt,
            "response": str(response),
            "persona": persona,
            "memory": memory
        })
        if hasattr(response, "__iter__") and not isinstance(response, str):
            response = "".join(list(response))
        return response

    except Exception as e:
        log_message(agent_id, f"Error in environment_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in environment_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"
