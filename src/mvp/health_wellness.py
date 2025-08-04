"""
VERN Health & Wellness Agent (Function-Based)
---------------------------------------------
Handles health, wellness, and medical queries for the MVP.
"""

from src.db.logger import log_action, log_message, log_gotcha

def health_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles health/wellness queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "health"
    try:
        log_action(agent_id, user_id, "health_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from src.mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Health & Wellness Agent. Provide health advice, wellness tips, and actionable recommendations.",
            "coach": "You are a health coach. Motivate, guide, and support the user toward wellness goals.",
            "medic": "You are a medical assistant. Provide evidence-based answers and recommend professional care when needed.",
            "mindfulness": "You are a mindfulness guide. Offer meditation, stress reduction, and mental health support.",
            "advisor": "You are a health advisor. Recommend actions and connect the user to relevant agents or plugins."
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
        log_message(agent_id, f"Error in health_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in health_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"
