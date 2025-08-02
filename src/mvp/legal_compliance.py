"""
VERN Legal & Compliance Agent (Function-Based)
----------------------------------------------
Handles compliance, contracts, and legal advice for the MVP.
"""

from db.logger import log_action, log_message, log_gotcha

def legal_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles legal/compliance queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "legal"
    try:
        log_action(agent_id, user_id, "legal_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Legal & Compliance Agent. Advise on compliance, contracts, and legal issues.",
            "advisor": "You are a legal advisor. Recommend actions and connect the user to relevant agents or plugins.",
            "analyst": "You are a legal analyst. Summarize trends, risks, and opportunities.",
            "reviewer": "You are a contract reviewer. Point out flaws, risks, and compliance issues.",
            "compliance": "You are a compliance officer. Ensure all actions meet legal and regulatory standards."
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
        log_message(agent_id, f"Error in legal_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in legal_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"
