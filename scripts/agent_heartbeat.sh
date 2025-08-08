#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://localhost:8000}"
NAME="${1:-orchestrator}"
CLUSTER="${2:-Orchestrator}"

# Capabilities as JSON array (default [])
CAPABILITIES_JSON_INPUT="${3:-[]}"
# Meta as JSON object (default {})
META_JSON_INPUT="${4:-{}}"

# Normalize inputs:
# - If CAPABILITIES_JSON_INPUT is not valid JSON, treat as comma-separated list
if echo "${CAPABILITIES_JSON_INPUT}" | jq -e . >/dev/null 2>&1; then
  CAPABILITIES_JSON="$(echo "${CAPABILITIES_JSON_INPUT}" | jq -c 'if type=="array" or type=="object" then . else [.] end')"
else
  IFS=',' read -ra PARTS <<< "${CAPABILITIES_JSON_INPUT}"
  # Build JSON array from parts, trimming empties
  CAPABILITIES_JSON="$(printf '%s\n' "${PARTS[@]}" | awk 'NF' | jq -R . | jq -s -c .)"
fi

# - If META_JSON_INPUT is not valid JSON, default to {}
if echo "${META_JSON_INPUT}" | jq -e . >/dev/null 2>&1; then
  META_JSON="$(echo "${META_JSON_INPUT}" | jq -c 'if type=="object" then . else {} end')"
else
  META_JSON='{}'
fi

payload=$(jq -nc --arg name "$NAME" --arg cluster "$CLUSTER" --argjson capabilities "${CAPABILITIES_JSON}" --argjson meta "${META_JSON}" \
  '{name:$name, cluster:$cluster, capabilities:$capabilities, meta:$meta}')

echo "[HEARTBEAT] POST ${API_BASE}/agents/heartbeat -> $payload"
curl -sSf -X POST "${API_BASE}/agents/heartbeat" \
  -H "Content-Type: application/json" \
  -d "${payload}"
echo