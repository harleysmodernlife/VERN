from fastapi import APIRouter, Body, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any

from vern_backend.app.privacy_policy import engine, PrivacyPolicyEngine
from vern_backend.app.errors import error_response

router = APIRouter(prefix="/privacy/policy", tags=["privacy"])

class EvaluateRequest(BaseModel):
    action: str
    user_id: str = "default_user"
    context: Dict[str, Any] = {}

class EvaluateResponse(BaseModel):
    policy_required: bool
    action: Optional[str] = None
    reason: Optional[str] = None
    request_id: Optional[str] = None
    suggested_scope: Optional[Dict[str, Any]] = None
    expires_at: Optional[float] = None

@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_policy(req: EvaluateRequest):
    # Basic validation and standardized error on empty action
    if not req.action or not isinstance(req.action, str):
        from fastapi import status
        from vern_backend.app.errors import error_response
        # No Request object here; envelope will omit request_id which is acceptable
        return error_response("VALIDATION_ERROR", status.HTTP_400_BAD_REQUEST, "action is required", None)
    required, payload = engine.evaluate(req.action, req.user_id, req.context)
    if not required:
        return EvaluateResponse(policy_required=False)
    # Ensure user_id is included for convenience
    payload["user_id"] = req.user_id
    return EvaluateResponse(**payload)

class DecisionRequest(BaseModel):
    request_id: str
    allowed: bool
    scope: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None
    user_id: str = "default_user"

class DecisionResponse(BaseModel):
    request_id: str
    action: str
    allowed: bool
    expires_at: Optional[float] = None
    reason: Optional[str] = None
    scope: Optional[Dict[str, Any]] = None

@router.post("/decision", response_model=DecisionResponse)
def policy_decision(req: DecisionRequest, request: Request):
    if not req.request_id:
        return error_response("VALIDATION_ERROR", status.HTTP_400_BAD_REQUEST, "request_id is required", request)
    decision = engine.record_decision(req.request_id, req.allowed, req.scope, req.reason)
    d = PrivacyPolicyEngine.to_dict(decision)
    # Audit: record decision
    try:
        from src.db.logger import log_action
        log_action(
            agent_id="orchestrator",
            user_id=req.user_id,
            action_type="privacy_decision",
            payload={
                "request_id": d["request_id"],
                "action": d["action"],
                "allowed": d["allowed"],
                "scope": d["scope"],
                "reason": d["reason"],
                "expires_at": d["expires_at"],
            },
            status="success"
        )
    except Exception:
        # Non-fatal
        pass
    return DecisionResponse(
        request_id=d["request_id"],
        action=d["action"],
        allowed=d["allowed"],
        expires_at=d["expires_at"],
        reason=d["reason"],
        scope=d["scope"],
    )