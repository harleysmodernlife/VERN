"""
VERN ID10T Monitor Agent (Function-Based)
-----------------------------------------
Handles error detection, troubleshooting, and diagnostics for the MVP.
"""

from db.logger import log_action, log_message, log_gotcha

def id10t_monitor_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles troubleshooting/error queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "id10t_monitor"
    try:
        log_action(agent_id, user_id, "id10t_monitor_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN ID10T Monitor Agent. Detect errors, troubleshoot issues, and provide actionable diagnostics.",
            "debugger": "You are a debugging expert. Trace problems and suggest fixes.",
            "mentor": "You are a troubleshooting mentor. Teach best practices and guide the user step-by-step.",
            "analyst": "You are an error analyst. Summarize trends, risks, and opportunities.",
            "advisor": "You are a diagnostics advisor. Recommend actions and connect the user to relevant agents or plugins."
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
        log_message(agent_id, f"Error in id10t_monitor_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in id10t_monitor_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"
