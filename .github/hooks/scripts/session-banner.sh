#!/bin/bash
set -euo pipefail

. "$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

if ! demo_hooks_enabled; then
  exit 0
fi

cat << 'EOF'
COPILOT DEMO HOOKS ACTIVE
-----------------------------------------------
- prompts may be logged locally for demo audit
- dangerous tool patterns may be blocked
- deterministic guardrails complement agent prompts
-----------------------------------------------
EOF
