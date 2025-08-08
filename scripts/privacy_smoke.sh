#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://localhost:8000}"
USER_ID="${USER_ID:-default_user}"

echo "[PRIVACY_SMOKE] API_BASE=${API_BASE} USER_ID=${USER_ID}"

fail() { echo "[PRIVACY_SMOKE][FAIL] $*"; exit 1; }
pass() { echo "[PRIVACY_SMOKE][PASS] $*"; }

# 1) Evaluate a non-sensitive action -> should not require policy
# Accept either compact or verbose response shapes; require policy_required=false.
echo "[PRIVACY_SMOKE] Evaluate non-sensitive (noop.action) ..."
resp="$(curl -sSf -X POST "${API_BASE}/privacy/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"noop.action\",\"user_id\":\"${USER_ID}\",\"context\":{}}")" || fail "evaluate non-sensitive failed"
echo "[PRIVACY_SMOKE] evaluate(non-sensitive) response: ${resp}"
echo "${resp}" | grep -q '"policy_required":\s*false' || fail "non-sensitive should report policy_required=false"
pass "non-sensitive OK"

# 2) Evaluate sensitive (web.fetch) -> should require policy
echo "[PRIVACY_SMOKE] Evaluate sensitive (web.fetch) ..."
resp="$(curl -sSf -X POST "${API_BASE}/privacy/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"web.fetch\",\"user_id\":\"${USER_ID}\",\"context\":{\"url\":\"https://example.com\"}}")" || fail "evaluate sensitive failed"
echo "[PRIVACY_SMOKE] evaluate(sensitive) response: ${resp}"
echo "${resp}" | grep -q '"policy_required":\s*true' || fail "sensitive should require policy"
REQ_ID="$(echo "${resp}" | sed -n 's/.*\"request_id\":\"\([^\"]\+\)\".*/\1/p' | head -n1)"
[ -n "${REQ_ID}" ] || fail "missing request_id"
pass "evaluate sensitive OK (request_id=${REQ_ID})"

# 3) Decision: allow
echo "[PRIVACY_SMOKE] Decision allow ..."
resp2="$(curl -sSf -X POST "${API_BASE}/privacy/policy/decision" \
  -H "Content-Type: application/json" \
  -d "{\"request_id\":\"${REQ_ID}\",\"allowed\":true,\"scope\":{\"auto_approve_session\":false},\"user_id\":\"${USER_ID}\"}")" || fail "decision allow failed"
echo "[PRIVACY_SMOKE] decision response: ${resp2}"
echo "${resp2}" | grep -q '"allowed":\s*true' || fail "decision allow did not persist"
pass "decision allow OK"

echo "[PRIVACY_SMOKE] All privacy checks passed."