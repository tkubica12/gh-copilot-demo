$ErrorActionPreference = "Stop"

. "$PSScriptRoot\common.ps1"

# Use ReadLine() not ReadToEnd() — VS Code Copilot Chat does not close stdin,
# so ReadToEnd() blocks forever. The JSON input is always a single line.
$inputText = [Console]::In.ReadLine()
$inputText = $inputText.Trim()
if ([string]::IsNullOrWhiteSpace($inputText)) {
    exit 0
}

$inputObj = $inputText | ConvertFrom-Json

$logDir = Get-HookLogsDirectory -ScriptRoot $PSScriptRoot
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$entry = @{
    event = "userPromptSubmitted"
    timestamp = $inputObj.timestamp
    cwd = $inputObj.cwd
} | ConvertTo-Json -Compress

Add-Content -Path "$logDir/audit.jsonl" -Value $entry
