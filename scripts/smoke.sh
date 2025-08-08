#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://localhost:8000}"

echo "[SMOKE] API_BASE=${API_BASE}"

fail() { echo "[SMOKE][FAIL] $*"; exit 1; }
pass() { echo "[SMOKE][PASS] $*"; }

# 1) Health
echo "[SMOKE] Checking /health ..."
curl -sSf "${API_BASE}/health" >/dev/null || fail "Health check failed"
pass "/health OK"

# 2) Agent status (used by Dashboard/Viz)
echo "[SMOKE] Checking /agents/status ..."
curl -sSf "${API_BASE}/agents/status" >/dev/null || fail "/agents/status failed"
pass "/agents/status OK"

# 3) Orchestrator basic request
echo "[SMOKE] Checking /agents/orchestrator/respond ..."
resp="$(curl -sSf -X POST "${API_BASE}/agents/orchestrator/respond" \
  -H "Content-Type: application/json" \
  -d '{"user_input":"smoke test","context":{"env":"smoke"}}' || true)"

echo "[SMOKE] Orchestrator response: ${resp}"
echo "${resp}" | grep -q "Orchestrator processed" || echo "[SMOKE][WARN] Orchestrator did not return expected phrase"

# 4) Registry: send two heartbeats with JSON payload and assert 'online'
if [[ -x "./scripts/agent_heartbeat.sh" ]]; then
  echo "[SMOKE] Sending agent heartbeats (new JSON payload) ..."
  ./scripts/agent_heartbeat.sh orchestrator Orchestrator '["registry","orchestration"]' '{"version":"0.1.0"}' || true
  sleep 1
  ./scripts/agent_heartbeat.sh orchestrator Orchestrator '["registry","orchestration"]' '{"version":"0.1.0"}' || true

  echo "[SMOKE] Verifying /agents/status shows orchestrator online ..."
  status_json="$(curl -sSf "${API_BASE}/agents/status" || true)"
  echo "[SMOKE] Status: ${status_json}"

  # Must contain orchestrator and be online
  online_count="$(echo "${status_json}" | jq '[.[] | select(.name=="orchestrator" and .status=="online")] | length' || echo 0)"
  [[ "${online_count}" -ge 1 ]] || fail "Orchestrator not online after heartbeat"

  pass "Registry status OK (orchestrator online)"
else
  echo "[SMOKE] Skipping registry heartbeat step (scripts/agent_heartbeat.sh not executable)"
fi

# 5) Standardized error envelope checks (non-fatal visibility)
echo "[SMOKE] Checking standardized error envelopes ..."
echo " - NOT_FOUND for integrations bogus provider"
curl -sS "${API_BASE}/integrations/bogus/status" | jq . || true

echo " - REGISTRY_NOT_FOUND when deleting non-existent agent"
curl -sS -X DELETE "${API_BASE}/agents/__nonexistent__" | jq . || true

echo " - VALIDATION_ERROR for privacy decision without request_id"
curl -sS -X POST "${API_BASE}/privacy/policy/decision" \
  -H "Content-Type: application/json" \
  -d '{}' | jq . || true

echo " - Admin DB verify"
curl -sS "${API_BASE}/admin/db/verify" | jq . || true

echo "[SMOKE] All checks executed."