[CmdletBinding()]
param(
    [string]$CatalogPath = "$PSScriptRoot\prompts.json",
    [string]$OutputDir = "$PSScriptRoot\runs",
    [string[]]$PromptId = @(),
    [string[]]$Model = @("auto"),
    [string[]]$Effort = @("medium"),
    [int]$Iterations = 1,
    [switch]$Execute,
    [switch]$AllowAllTools
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path $CatalogPath)) {
    throw "Prompt catalog not found: $CatalogPath"
}

$catalog = Get-Content -Path $CatalogPath -Raw | ConvertFrom-Json
$prompts = @($catalog.prompts)
if ($PromptId.Count -gt 0) {
    $selected = New-Object System.Collections.Generic.HashSet[string] ([StringComparer]::OrdinalIgnoreCase)
    foreach ($id in $PromptId) {
        [void]$selected.Add($id)
    }
    $prompts = @($prompts | Where-Object { $selected.Contains($_.id) })
}

if ($prompts.Count -eq 0) {
    throw "No prompts selected. Check -PromptId values or the catalog."
}

$OutputDir = (New-Item -ItemType Directory -Force -Path $OutputDir).FullName

$copilotCommand = Get-Command copilot -ErrorAction SilentlyContinue
if (-not $copilotCommand) {
    throw "GitHub Copilot CLI was not found on PATH."
}

$results = @()
foreach ($prompt in $prompts) {
    $promptModels = @($Model)
    if ($prompt.PSObject.Properties.Name -contains "models") {
        $promptModels = @($prompt.models)
    }
    $promptEfforts = @($Effort)
    if ($prompt.PSObject.Properties.Name -contains "efforts") {
        $promptEfforts = @($prompt.efforts)
    }

    foreach ($modelName in $promptModels) {
        foreach ($effortName in $promptEfforts) {
            for ($iteration = 1; $iteration -le $Iterations; $iteration++) {
            $runId = "{0}-{1}-{2}-{3:000}-{4}" -f $prompt.id, $modelName, $effortName, $iteration, (Get-Date -Format "yyyyMMddHHmmss")
            $runDir = (New-Item -ItemType Directory -Force -Path (Join-Path $OutputDir $runId)).FullName

            $otelPath = Join-Path $runDir "copilot-otel.jsonl"
            $stdoutPath = Join-Path $runDir "stdout.jsonl"
            $stderrPath = Join-Path $runDir "stderr.txt"
            $metadataPath = Join-Path $runDir "metadata.json"

            $metadata = [ordered]@{
                runId = $runId
                promptId = $prompt.id
                promptName = $prompt.name
                expectedTechnique = $prompt.expectedTechnique
                comparisonGroup = if ($prompt.PSObject.Properties.Name -contains "comparisonGroup") { $prompt.comparisonGroup } else { "" }
                variant = if ($prompt.PSObject.Properties.Name -contains "variant") { $prompt.variant } else { "" }
                baseline = if ($prompt.PSObject.Properties.Name -contains "baseline") { [bool]$prompt.baseline } else { $false }
                model = $modelName
                effort = $effortName
                mode = $prompt.mode
                iteration = $iteration
                execute = [bool]$Execute
                startedAt = (Get-Date).ToString("o")
                otelPath = $otelPath
                stdoutPath = $stdoutPath
                stderrPath = $stderrPath
            }
            $metadata | ConvertTo-Json -Depth 10 | Set-Content -Path $metadataPath -Encoding UTF8

            if (-not $Execute) {
                "[DRY RUN] copilot -p <prompt> --output-format json --stream off --mode $($prompt.mode) --model $modelName --reasoning-effort $effortName" |
                    Set-Content -Path $stdoutPath -Encoding UTF8
                New-Item -ItemType File -Force -Path $otelPath | Out-Null
                New-Item -ItemType File -Force -Path $stderrPath | Out-Null
                $results += [pscustomobject]@{
                    runId = $runId
                    promptId = $prompt.id
                    model = $modelName
                    effort = $effortName
                    exitCode = 0
                    elapsedSeconds = 0
                    dryRun = $true
                }
                continue
            }

            $oldOtelPath = $env:COPILOT_OTEL_FILE_EXPORTER_PATH
            $oldOtelEnabled = $env:COPILOT_OTEL_ENABLED
            $oldResourceAttributes = $env:OTEL_RESOURCE_ATTRIBUTES
            try {
                $env:COPILOT_OTEL_FILE_EXPORTER_PATH = $otelPath
                $env:COPILOT_OTEL_ENABLED = "true"
                $env:OTEL_RESOURCE_ATTRIBUTES = "repo=gh-copilot-demo,experiment=copilot-token-lab,prompt.id=$($prompt.id),technique=$($prompt.expectedTechnique)"

                $arguments = @(
                    "-p", $prompt.prompt,
                    "--output-format", "json",
                    "--stream", "off",
                    "--mode", $prompt.mode,
                    "--no-ask-user",
                    "--log-level", "none"
                )

                if ($modelName -and $modelName -ne "auto") {
                    $arguments += @("--model", $modelName)
                }
                if ($effortName) {
                    $arguments += @("--reasoning-effort", $effortName)
                }
                if ($AllowAllTools) {
                    $arguments += "--allow-all-tools"
                }
                if (
                    ($prompt.PSObject.Properties.Name -contains "noCustomInstructions") -and
                    [bool]$prompt.noCustomInstructions
                ) {
                    $arguments += "--no-custom-instructions"
                }
                if (
                    ($prompt.PSObject.Properties.Name -contains "disableBuiltinMcps") -and
                    [bool]$prompt.disableBuiltinMcps
                ) {
                    $arguments += "--disable-builtin-mcps"
                }
                if ($prompt.PSObject.Properties.Name -contains "availableTools") {
                    $arguments += "--available-tools"
                    $arguments += ($prompt.availableTools -join ",")
                }
                if ($prompt.PSObject.Properties.Name -contains "additionalMcpConfig") {
                    $mcpConfigPath = (Resolve-Path $prompt.additionalMcpConfig).Path
                    $arguments += @("--additional-mcp-config", "@$mcpConfigPath")
                }
                if ($prompt.PSObject.Properties.Name -contains "extraArgs") {
                    $arguments += @($prompt.extraArgs)
                }

                $timer = [System.Diagnostics.Stopwatch]::StartNew()
                $workingDirectory = if ($prompt.PSObject.Properties.Name -contains "workingDirectory") { $prompt.workingDirectory } else { "" }
                if ($workingDirectory) {
                    Push-Location $workingDirectory
                    try {
                        & copilot @arguments 1> $stdoutPath 2> $stderrPath
                        $exitCode = $LASTEXITCODE
                    }
                    finally {
                        Pop-Location
                    }
                }
                else {
                    & copilot @arguments 1> $stdoutPath 2> $stderrPath
                    $exitCode = $LASTEXITCODE
                }
                $timer.Stop()

                $results += [pscustomobject]@{
                    runId = $runId
                    promptId = $prompt.id
                    model = $modelName
                    effort = $effortName
                    exitCode = $exitCode
                    elapsedSeconds = [Math]::Round($timer.Elapsed.TotalSeconds, 3)
                    dryRun = $false
                }
            }
            finally {
                $env:COPILOT_OTEL_FILE_EXPORTER_PATH = $oldOtelPath
                $env:COPILOT_OTEL_ENABLED = $oldOtelEnabled
                $env:OTEL_RESOURCE_ATTRIBUTES = $oldResourceAttributes
            }
        }
    }
    }
}

$summaryPath = Join-Path $OutputDir "run-summary.json"
$results | ConvertTo-Json -Depth 10 | Set-Content -Path $summaryPath -Encoding UTF8
Write-Output "Wrote run summary: $summaryPath"
Write-Output "Analyze telemetry with: python $PSScriptRoot\analyze_otel.py --runs $OutputDir --output $OutputDir\analysis.md"
