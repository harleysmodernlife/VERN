"""
agent_utils.py

Shared utilities for agent logging and error escalation in VERN.
Use these functions in all agents to standardize logging and escalation patterns.
"""

from src.db.logger import log_action, log_message, log_gotcha

def log_agent_action(agent_id, user_id, action_type, details, status="started"):
    """
    Standardized agent action logging.
    """
    log_action(agent_id, user_id, action_type, details, status=status)

def log_agent_message(agent_id, message, level="info", context=None):
    """
    Standardized agent message logging.
    """
    log_message(agent_id, message, level=level, context=context or {})

def log_agent_exception(agent_id, exception_msg, severity="error"):
    """
    Standardized agent exception logging.
    """
    log_gotcha(agent_id, exception_msg, severity=severity)

def escalate_to_orchestrator(error_msg, error_context, agent_status=None, user_id="default_user"):
    """
    Standardized error escalation to orchestrator.
    """
    from src.mvp.orchestrator import orchestrator_respond
    return orchestrator_respond(error_msg, error_context, agent_status, user_id)
