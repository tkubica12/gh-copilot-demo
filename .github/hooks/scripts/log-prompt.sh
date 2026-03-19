#!/bin/bash
set -euo pipefail

. "$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

INPUT="$(cat)"
if [ -z "${INPUT//[[:space:]]/}" ]; then
  exit 0
fi

LOG_DIR="$(hook_logs_dir)"
mkdir -p "$LOG_DIR"

TIMESTAMP="$(echo "$INPUT" | jq -r '.timestamp // empty')"
CWD="$(echo "$INPUT" | jq -r '.cwd // empty')"

jq -n \
  --arg event "userPromptSubmitted" \
  --arg ts "$TIMESTAMP" \
  --arg cwd "$CWD" \
  '{event: $event, timestamp: $ts, cwd: $cwd}' >> "$LOG_DIR/audit.jsonl"
