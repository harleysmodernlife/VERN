"""
VERN Admin Agent (Function-Based)
---------------------------------
Handles scheduling, reminders, and administrative tasks for the MVP.
"""

from src.db.logger import log_action, log_message, log_gotcha

def admin_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles admin/scheduling queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "admin"
    try:
        log_action(agent_id, user_id, "admin_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from src.mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Admin Agent. Schedule tasks, set reminders, and manage administrative actions.",
            "scheduler": "You are a scheduling expert. Optimize calendars and deadlines.",
            "reminder": "You are a reminder bot. Help the user remember important tasks and events.",
            "assistant": "You are a personal assistant. Organize, prioritize, and support the user.",
            "advisor": "You are an admin advisor. Recommend actions and connect the user to relevant agents or plugins."
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
        log_message(agent_id, f"Error in admin_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in admin_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"

class Admin:
    """
    Class-based Admin agent for compatibility with orchestration and MCP server.
    """
    def schedule_meeting(self, details, user_id=None):
        """
        Schedule a meeting or event.
        """
        context = {"details": details}
        return admin_respond(details, context=context, persona="scheduler", user_id=user_id)
