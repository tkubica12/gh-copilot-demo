#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.toolName // .tool_name // empty')"
TOOL_ARGS="$(echo "$INPUT" | jq -r '.toolArgs // empty')"

if [ "$TOOL_NAME" != "bash" ] && [ "$TOOL_NAME" != "powershell" ]; then
  exit 0
fi

if echo "$TOOL_ARGS" | grep -qiE 'rm -rf /|mkfs|format|DROP TABLE|curl.+\|.+bash|wget.+\|.+sh'; then
  jq -n \
    --arg decision "deny" \
    --arg reason "Blocked by workshop hook policy: destructive or download-and-execute pattern detected." \
    '{permissionDecision: $decision, permissionDecisionReason: $reason}'
fi
