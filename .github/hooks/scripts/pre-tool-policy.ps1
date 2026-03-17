$ErrorActionPreference = "Stop"

$inputText = [Console]::In.ReadToEnd()
$inputObj = $inputText | ConvertFrom-Json

$toolName = if ($null -ne $inputObj.toolName) { $inputObj.toolName } elseif ($null -ne $inputObj.tool_name) { $inputObj.tool_name } else { "" }
$toolArgs = if ($null -ne $inputObj.toolArgs) { [string]$inputObj.toolArgs } else { "" }

if ($toolName -notin @("bash", "powershell")) {
    exit 0
}

$dangerous = @(
    'rm\s+-rf\s+/',
    'mkfs',
    'format',
    'DROP TABLE',
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
