#!/bin/bash
set -euo pipefail

# Consume stdin — Copilot pipes JSON context to every hook.
# Without this, the pipe blocks and the session hangs.
cat > /dev/null

cat << 'EOF'
COPILOT DEMO HOOKS ACTIVE
-----------------------------------------------
- prompts may be logged locally for demo audit
- dangerous tool patterns may be blocked
- deterministic guardrails complement agent prompts
-----------------------------------------------
EOF
exit 0
