"""
VERN Security & Privacy Agent (Function-Based)
----------------------------------------------
Handles privacy, security, and monitoring for the MVP.
"""

from db.logger import log_action, log_message, log_gotcha

def security_privacy_monitor_action(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles security/privacy queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "security"
    try:
        log_action(agent_id, user_id, "security_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Security & Privacy Agent. Monitor privacy, security, and system health.",
            "advisor": "You are a security advisor. Recommend actions and connect the user to relevant agents or plugins.",
            "analyst": "You are a security analyst. Summarize risks, threats, and vulnerabilities.",
            "auditor": "You are a privacy auditor. Point out flaws, risks, and compliance issues.",
            "monitor": "You are a systems monitor. Track metrics and alert the user to issues."
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
        log_message(agent_id, f"Error in security_privacy_monitor_action: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in security_privacy_monitor_action: {str(e)}", severity="error")
        return f"Error: {str(e)}"
