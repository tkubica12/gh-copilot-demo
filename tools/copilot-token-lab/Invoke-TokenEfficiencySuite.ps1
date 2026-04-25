[CmdletBinding()]
param(
    [string]$OutputDir = "$PSScriptRoot\suite-runs",
    [int]$Iterations = 1,
    [switch]$Execute,
    [switch]$AllowAllTools
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$OutputDir = (New-Item -ItemType Directory -Force -Path $OutputDir).FullName
$workspaceDir = Join-Path $OutputDir "scenario-workspaces"
$catalogPath = python "$PSScriptRoot\scenario_builder.py" --output $workspaceDir
if ($LASTEXITCODE -ne 0) {
    throw "Scenario generation failed."
}

$runDir = Join-Path $OutputDir "runs"
$invokeArgs = @{
    CatalogPath = $catalogPath
    OutputDir = $runDir
    Iterations = $Iterations
}
if ($Execute) {
    $invokeArgs.Execute = $true
}
if ($AllowAllTools) {
    $invokeArgs.AllowAllTools = $true
}

& "$PSScriptRoot\Invoke-CopilotTokenLab.ps1" @invokeArgs
if ($LASTEXITCODE -ne 0) {
    throw "Token lab execution failed."
}

$analysisPath = Join-Path $OutputDir "analysis.md"
python "$PSScriptRoot\analyze_otel.py" --runs $runDir --output $analysisPath
if ($LASTEXITCODE -ne 0) {
    throw "Analysis failed."
}

Write-Output "Scenario catalog: $catalogPath"
Write-Output "Analysis: $analysisPath"
