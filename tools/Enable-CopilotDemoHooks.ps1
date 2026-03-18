$ErrorActionPreference = "Stop"

$flagPath = Join-Path $PSScriptRoot "..\.github\hooks\demo-enabled.flag"
$resolvedFlagPath = [System.IO.Path]::GetFullPath($flagPath)
$flagDirectory = Split-Path -Parent $resolvedFlagPath

if (-not (Test-Path $flagDirectory)) {
    throw "Hook directory not found: $flagDirectory"
}

Set-Content -Path $resolvedFlagPath -Value "enabled" -NoNewline

Write-Host "Copilot demo hooks enabled."
Write-Host "Flag file: $resolvedFlagPath"
Write-Host "Remember to run .\tools\Disable-CopilotDemoHooks.ps1 after the hooks section."
