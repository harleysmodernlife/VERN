#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://localhost:8000}"
export API_BASE

echo "[FULL_SMOKE] Using API_BASE=${API_BASE}"

fail() { echo "[FULL_SMOKE][FAIL] $*"; exit 1; }
pass() { echo "[FULL_SMOKE][PASS] $*"; }

# Run core smoke (health, status, orchestrator basic + registry heartbeat assertions + envelope checks)
if [[ -x "./scripts/smoke.sh" ]]; then
  echo "[FULL_SMOKE] Running core smoke tests..."
  ./scripts/smoke.sh
else
  echo "[FULL_SMOKE][WARN] scripts/smoke.sh not executable or missing; skipping core smoke"
fi

# Run privacy smoke (evaluate + decision)
if [[ -x "./scripts/privacy_smoke.sh" ]]; then
  echo "[FULL_SMOKE] Running privacy smoke tests..."
  ./scripts/privacy_smoke.sh
else
  echo "[FULL_SMOKE][WARN] scripts/privacy_smoke.sh not executable or missing; skipping privacy smoke"
fi

# Assert standardized envelope shapes on selected negative paths
echo "[FULL_SMOKE] Verifying standardized error envelopes ..."
int_resp="$(curl -sS "${API_BASE}/integrations/bogus/status" || true)"
echo "${int_resp}" | jq .
echo "${int_resp}" | jq -e '.ok==false and .error_code=="NOT_FOUND"' >/dev/null || fail "Expected NOT_FOUND envelope for bogus integration"

del_resp="$(curl -sS -X DELETE "${API_BASE}/agents/__nonexistent__" || true)"
echo "${del_resp}" | jq .
echo "${del_resp}" | jq -e '.ok==false and .error_code=="REGISTRY_NOT_FOUND"' >/dev/null || fail "Expected REGISTRY_NOT_FOUND on delete nonexistent agent"

priv_resp="$(curl -sS -X POST "${API_BASE}/privacy/policy/decision" -H "Content-Type: application/json" -d '{}' || true)"
echo "${priv_resp}" | jq .
echo "${priv_resp}" | jq -e '.ok==false and .error_code=="VALIDATION_ERROR"' >/dev/null || fail "Expected VALIDATION_ERROR for missing request_id"

db_resp="$(curl -sS "${API_BASE}/admin/db/verify" || true)"
echo "${db_resp}" | jq .
echo "${db_resp}" | jq -e '(.ok==true) or (.ok==false and (.error_code=="DB_UNAVAILABLE" or .error_code=="UNKNOWN_ERROR"))' >/dev/null || fail "Unexpected /admin/db/verify response"

pass "Standardized envelope checks passed"
echo "[FULL_SMOKE] Completed."