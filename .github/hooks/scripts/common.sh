#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOK_FLAG="$HOOK_ROOT/demo-enabled.flag"
HOOK_LOG_DIR="$HOOK_ROOT/logs"

demo_hooks_enabled() {
  local env_value="${COPILOT_DEMO_HOOKS:-}"
  env_value="$(echo "$env_value" | tr '[:upper:]' '[:lower:]')"

  if [ "$env_value" = "1" ] || [ "$env_value" = "true" ] || [ "$env_value" = "yes" ] || [ "$env_value" = "on" ]; then
    return 0
  fi

  [ -f "$HOOK_FLAG" ]
}

hook_logs_dir() {
  echo "$HOOK_LOG_DIR"
}
