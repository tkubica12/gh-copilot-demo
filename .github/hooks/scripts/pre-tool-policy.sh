#!/bin/bash
set -euo pipefail

. "$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

INPUT="$(cat)"
if [ -z "${INPUT//[[:space:]]/}" ]; then
  exit 0
fi

TOOL_NAME="$(echo "$INPUT" | jq -r '.toolName // .tool_name // empty')"
TOOL_ARGS="$(echo "$INPUT" | jq -rc '(.toolArgs // .tool_args // .input // empty) | if type == "string" then . else tostring end')"

if [ "$TOOL_NAME" != "bash" ] && [ "$TOOL_NAME" != "powershell" ]; then
  exit 0
fi

if echo "$TOOL_ARGS" | grep -qiE '(^|[[:space:]])rm[[:space:]]+-rf([[:space:]]|$)|Remove-Item.*-Recurse.*-Force|Remove-Item.*-Force.*-Recurse|(^|[[:space:]])mkfs([[:space:]]|$)|(^|[[:space:]])format(\.com)?([[:space:]]|$)|Format-Volume|DROP[[:space:]]+TABLE|git[[:space:]]+push[[:space:]].*(--force(-with-lease)?|-f)($|[[:space:]])|curl.+\|.+bash|wget.+\|.+sh'; then
  jq -n \
    --arg decision "deny" \
    --arg reason "Blocked by workshop hook policy: destructive or download-and-execute pattern detected." \
    '{permissionDecision: $decision, permissionDecisionReason: $reason}'
fi
