"""
VERN Finance & Resource Agent (Function-Based)
----------------------------------------------
Handles budgeting, resource allocation, and financial planning for the MVP.
"""

from db.logger import log_action, log_message, log_gotcha

def finance_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles finance/resource queries with persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "finance"
    try:
        log_action(agent_id, user_id, "finance_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Finance & Resource Agent. Provide budgeting, resource allocation, and financial planning advice.",
            "planner": "You are a financial planner. Create actionable budgets and savings plans.",
            "analyst": "You are a financial analyst. Summarize trends, risks, and opportunities.",
            "advisor": "You are a finance advisor. Recommend actions and connect the user to relevant agents or plugins.",
            "auditor": "You are a strict auditor. Point out flaws, risks, and compliance issues."
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
        log_message(agent_id, f"Error in finance_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in finance_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"
