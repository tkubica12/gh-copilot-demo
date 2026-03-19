$ErrorActionPreference = "Stop"

. "$PSScriptRoot\common.ps1"

$inputText = [Console]::In.ReadToEnd()
$inputText = $inputText.Trim()
if ([string]::IsNullOrWhiteSpace($inputText)) {
    exit 0
}

$inputObj = $inputText | ConvertFrom-Json

$toolName = if ($null -ne $inputObj.toolName) { $inputObj.toolName } elseif ($null -ne $inputObj.tool_name) { $inputObj.tool_name } else { "" }
$toolArgsValue = if ($null -ne $inputObj.toolArgs) { $inputObj.toolArgs } elseif ($null -ne $inputObj.tool_args) { $inputObj.tool_args } elseif ($null -ne $inputObj.input) { $inputObj.input } else { $null }
$toolArgs = Convert-HookValueToText -Value $toolArgsValue

if ($toolName -notin @("bash", "powershell")) {
    exit 0
}

$dangerous = @(
    '(?<!\S)rm\s+-rf(?:\s+|$)',
    'Remove-Item\b(?=.*(?:^|\s)-Recurse(?:\s|$))(?=.*(?:^|\s)-Force(?:\s|$))',
    '(?<!\S)mkfs(?:\s+|$)',
    '(?<!\S)format(?:\.com)?(?:\s+|$)',
    'Format-Volume\b',
    'DROP\s+TABLE\b',
    'git\s+push\s+.*(?:--force(?:-with-lease)?|-f)\b',
    'curl.+\|.+bash',
    'wget.+\|.+sh'
)

foreach ($pattern in $dangerous) {
    if ($toolArgs -match $pattern) {
        @{
            permissionDecision = "deny"
            permissionDecisionReason = "Blocked by workshop hook policy: destructive or download-and-execute pattern detected."
        } | ConvertTo-Json -Compress
        exit 0
    }
}
