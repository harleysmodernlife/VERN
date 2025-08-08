import os
import uuid
import time
from dataclasses import dataclass, asdict
from typing import Dict, Optional, Tuple


# First-pass sensitive actions
SENSITIVE_ACTIONS = {"file.read", "file.write", "web.fetch", "email.send"}

DEFAULT_DECISION_TTL_SECONDS = int(os.getenv("PRIVACY_DECISION_TTL_SECONDS", "600"))  # 10 minutes


@dataclass
class PolicyDecision:
    request_id: str
    action: str
    allowed: bool
    reason: Optional[str]
    scope: Optional[dict]
    decided_at: float
    expires_at: Optional[float]


class PrivacyPolicyEngine:
    """
    Minimal in-memory privacy policy engine with ephemeral decision cache.
    - evaluate(action, user_id, context) returns (policy_required, payload)
    - record_decision(request_id, allowed, scope, reason) stores a decision
    - check_cached_decision(action) returns an existing decision if not expired

    TODO: Add persistent audit trail for all privacy decisions (privacy audits).
    TODO: Implement consent management and data export for user requests.
    """
    def __init__(self, decision_ttl_seconds: int = DEFAULT_DECISION_TTL_SECONDS):
        self.decision_ttl_seconds = decision_ttl_seconds
        self._pending: Dict[str, Dict] = {}     # request_id -> payload
        self._decisions: Dict[str, PolicyDecision] = {}  # request_id -> decision
        self._audit_log: list = []  # Compartmentalized privacy audit log

    def _now(self) -> float:
        return time.time()

    def _mk_request_id(self) -> str:
        return uuid.uuid4().hex

    def _expired(self, expires_at: Optional[float]) -> bool:
        if not expires_at:
            return False
        return self._now() > expires_at

    def evaluate(self, action: str, user_id: str, context: Optional[dict] = None) -> Tuple[bool, Dict]:
        """
        Evaluate an action. If not sensitive, return (False, {}).
        If sensitive, return (True, { policy_required: True, ... }) with suggested scope and reason.
        """
        if action not in SENSITIVE_ACTIONS:
            return False, {}

        # If we find a recent allowed decision for the same action and user, we could auto-allow.
        # For the MVP, require consent each time; later we can key by (user_id, action, scope).
        request_id = self._mk_request_id()
        reason = f"Action '{action}' requires explicit user consent."
        suggested_scope = {"action": action, "duration": "session", "constraints": context or {}}
        payload = {
            "policy_required": True,
            "action": action,
            "reason": reason,
            "request_id": request_id,
            "suggested_scope": suggested_scope,
            "expires_at": None,  # front-end may ignore or set
        }
        self._pending[request_id] = {
            "user_id": user_id,
            "action": action,
            "context": context or {},
            "created_at": self._now(),
        }
        return True, payload

    def record_decision(self, request_id: str, allowed: bool, scope: Optional[dict] = None, reason: Optional[str] = None) -> PolicyDecision:
        """
        Store a user decision for a pending request. Returns the decision object.
        Also logs the decision to the compartmentalized privacy audit log.
        """
        info = self._pending.pop(request_id, None)
        action = info["action"] if info else "unknown"
        decided_at = self._now()
        expires_at = decided_at + self.decision_ttl_seconds if allowed else None
        decision = PolicyDecision(
            request_id=request_id,
            action=action,
            allowed=allowed,
            reason=reason,
            scope=scope,
            decided_at=decided_at,
            expires_at=expires_at,
        )
        self._decisions[request_id] = decision
        # Compartmentalized privacy audit log entry
        self._audit_log.append({
            "request_id": request_id,
            "action": action,
            "allowed": allowed,
            "reason": reason,
            "scope": scope,
            "decided_at": decided_at,
            "expires_at": expires_at,
            "user_id": info["user_id"] if info and "user_id" in info else None,
        })
        # TODO: Persist audit log to external storage for privacy audits
        return decision

    def get_decision(self, request_id: str) -> Optional[PolicyDecision]:
        """
        Lookup a recorded decision by id.
        """
        d = self._decisions.get(request_id)
        if d and not self._expired(d.expires_at):
            return d
        return None

    def clear_expired(self):
        """
        GC expired decisions.
        """
        now = self._now()
        to_delete = []
        for rid, d in self._decisions.items():
            if d.expires_at and now > d.expires_at:
                to_delete.append(rid)
        for rid in to_delete:
            self._decisions.pop(rid, None)

    @staticmethod
    def to_dict(decision: PolicyDecision) -> Dict:
        d = asdict(decision)
        # ensure JSON friendly floats
        if d.get("decided_at"):
            d["decided_at"] = float(d["decided_at"])
        if d.get("expires_at"):
            d["expires_at"] = float(d["expires_at"])
        return d


# Singleton engine
engine = PrivacyPolicyEngine()

def get_privacy_audit_log():
    """
    Returns the compartmentalized privacy audit log.
    TODO: Add filtering by user_id, action, or time for frontend audit trail.
    """
    return engine._audit_log