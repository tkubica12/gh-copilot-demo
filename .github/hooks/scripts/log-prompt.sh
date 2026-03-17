#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
LOG_DIR=".github/hooks/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP="$(echo "$INPUT" | jq -r '.timestamp // empty')"
CWD="$(echo "$INPUT" | jq -r '.cwd // empty')"

jq -n \
  --arg event "userPromptSubmitted" \
  --arg ts "$TIMESTAMP" \
  --arg cwd "$CWD" \
  '{event: $event, timestamp: $ts, cwd: $cwd}' >> "$LOG_DIR/audit.jsonl"
