$ErrorActionPreference = "Stop"

$flagPath = Join-Path $PSScriptRoot "..\.github\hooks\demo-enabled.flag"
$resolvedFlagPath = [System.IO.Path]::GetFullPath($flagPath)

if (Test-Path $resolvedFlagPath) {
    Remove-Item -Path $resolvedFlagPath -Force
    Write-Host "Copilot demo hooks disabled."
    Write-Host "Removed flag file: $resolvedFlagPath"
}
else {
    Write-Host "Copilot demo hooks were already disabled."
}
