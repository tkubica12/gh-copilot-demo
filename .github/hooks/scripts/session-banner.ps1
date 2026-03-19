$ErrorActionPreference = "Stop"

# Use ReadLine() not ReadToEnd() — VS Code Copilot Chat does not close stdin,
# so ReadToEnd() blocks forever. The JSON input is always a single line.
[Console]::In.ReadLine() | Out-Null

Write-Host @"
COPILOT DEMO HOOKS ACTIVE
-----------------------------------------------
- Prompts may be logged locally for demo audit
- Dangerous tool patterns may be blocked
- Deterministic guardrails complement agent prompts
-----------------------------------------------
"@
exit 0
