$ErrorActionPreference = "Stop"

. "$PSScriptRoot\common.ps1"

if (-not (Test-DemoHooksEnabled -ScriptRoot $PSScriptRoot)) {
    exit 0
}

Write-Host @"
COPILOT DEMO HOOKS ACTIVE
-----------------------------------------------
- prompts may be logged locally for demo audit
- dangerous tool patterns may be blocked
- deterministic guardrails complement agent prompts
-----------------------------------------------
"@
