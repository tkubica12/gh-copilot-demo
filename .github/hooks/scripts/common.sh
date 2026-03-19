#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOK_LOG_DIR="$HOOK_ROOT/logs"

hook_logs_dir() {
  echo "$HOOK_LOG_DIR"
}
