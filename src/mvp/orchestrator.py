"""
VERN Orchestrator (Function-Based)
----------------------------------
Coordinates communication between agents, handles error escalation,
processes and refines context data, adjusts agent parameters based on
aggregated feedback, and aggregates multi-agent workflows.
"""

from src.db.logger import log_action, log_message, log_gotcha

def process_context(context):
    """
    Refine and tailor the raw context data for more effective downstream usage.
    This function cleans string values and leaves other types unchanged.
    """
    if context and isinstance(context, dict):
        refined = {}
        for key, value in context.items():
            if isinstance(value, str):
                # Example refinement: trim whitespace and standardize capitalization.
                refined[key] = value.strip().capitalize()
            else:
                refined[key] = value
        return refined
    return context

def adjust_agent_parameters(feedback_data):
    """
    Adjust agent parameters dynamically based on aggregated feedback.
    For demonstration, if the negative feedback ratio exceeds a threshold,
    recommend reviewing agent configurations.
    
    In production, this mechanism could automatically tune parameters.
    """
    threshold = 0.5
    neg_ratio = feedback_data.get("negative_ratio", 0)
    if neg_ratio > threshold:
        recommendation = (
            "High negative feedback detected (ratio: "
            f"{neg_ratio:.2f}). Consider tuning agent parameters."
        )
        # In a real system, adjustments would be applied here.
        return recommendation
    return "Agent parameters are optimal."

def orchestrator_respond(user_input, context=None, agent_status=None, user_id="default_user"):
    """
    Routes the input to appropriate agent clusters, aggregates responses,
    refines per-agent context data, optionally adjusts agent parameters based
    on dynamic feedback, and handles error escalation.
    
    If the context includes a 'feedback' key with aggregated feedback data,
    the orchestrator will invoke dynamic parameter adjustment.
    """
    agent_id = "orchestrator"
    try:
        # Process and refine the raw context before proceeding.
        refined_context = process_context(context)

        log_action(agent_id, user_id, "orchestrator_request", {
            "user_input": user_input,
            "context": refined_context,
            "agent_status": agent_status
        }, status="started")
        
        # Simulated multi-agent aggregated response.
        response = f"Orchestrator processed: {user_input}\nContext: {refined_context}\nStatus: {agent_status}"
        
        # If a specific error flag is in the context, log a warning.
        if refined_context and isinstance(refined_context, dict) and refined_context.get("error"):
            error_detail = refined_context.get("error")
            log_message(agent_id, f"Detected error in upstream agent: {error_detail}", level="warning")
            response += f"\nWarning: Upstream error detected - {error_detail}"
        
        # If aggregated feedback is provided in the context, adjust agent parameters.
        if refined_context and isinstance(refined_context, dict) and "feedback" in refined_context:
            feedback_data = refined_context["feedback"]
            recommendation = adjust_agent_parameters(feedback_data)
            response += f"\nParameter Recommendation: {recommendation}"
        
        log_action(agent_id, user_id, "orchestrator_response", {
            "response": response,
            "context": refined_context
        })
        return response

    except Exception as e:
        error_msg = f"Orchestrator encountered an error: {str(e)}"
        log_message(agent_id, error_msg, level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status
        })
        log_gotcha(agent_id, error_msg, severity="critical")
        return error_msg

# Additional orchestration functions (e.g., workflow aggregation, agent chaining) can be added here.

# --- Workflow & Agent Chaining ---

WORKFLOWS = {}

def create_workflow(name, steps):
    """
    Create a new workflow.
    Args:
        name: Workflow name.
        steps: List of agent call dicts, e.g. [{"agent": "research", "input": "..."}]
    """
    WORKFLOWS[name] = steps
    return f"Workflow '{name}' created with {len(steps)} steps."

def list_workflows():
    """
    List all available workflows.
    Returns:
        Dict of workflow names and steps.
    """
    return WORKFLOWS

async def run_workflow(name, initial_input=None, user_id="default_user"):
    """
    Execute a workflow by chaining agent calls. This is now async.
    Args:
        name: Workflow name.
        initial_input: Optional input for the first agent.
        user_id: User ID for logging.
    Returns:
        Aggregated output from all agents as a JSON-serializable list.
    """
    steps = WORKFLOWS.get(name)
    if not steps:
        return f"Workflow '{name}' not found."

    output = initial_input
    results = []
    for idx, step in enumerate(steps):
        agent = step.get("agent")
        agent_input = step.get("input", output)
        
        try:
            # Dynamically import and call the agent's respond function
            # This is a simplified example; a real implementation would use a registry
            if agent == "research":
                from src.mvp.research import research_respond
                result_maybe_async = research_respond(agent_input, user_id=user_id)
            elif agent == "finance":
                from src.mvp.finance_resource import finance_respond
                result_maybe_async = finance_respond(agent_input, user_id=user_id)
            elif agent == "health":
                from src.mvp.health_wellness import health_respond
                result_maybe_async = health_respond(agent_input, user_id=user_id)
            else:
                result_maybe_async = f"Agent '{agent}' not implemented."

            # Normalize the result here
            from vern_backend.app.agents import _normalize_result
            result = await _normalize_result(result_maybe_async)
            
            output = result
            results.append({"step": idx + 1, "agent": agent, "output": result})
        except Exception as e:
            results.append({"step": idx + 1, "agent": agent, "error": str(e)})
            break
            
    return results
