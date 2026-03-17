$ErrorActionPreference = "Stop"

$inputText = [Console]::In.ReadToEnd()
$inputObj = $inputText | ConvertFrom-Json

$logDir = ".github/hooks/logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$entry = @{
    event = "userPromptSubmitted"
    timestamp = $inputObj.timestamp
    cwd = $inputObj.cwd
} | ConvertTo-Json -Compress

Add-Content -Path "$logDir/audit.jsonl" -Value $entry
