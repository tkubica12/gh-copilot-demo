$ErrorActionPreference = "Stop"

function Get-HookRoot {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptRoot
    )

    return (Split-Path -Parent $ScriptRoot)
}

function Get-HookFlagPath {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptRoot
    )

    return (Join-Path (Get-HookRoot -ScriptRoot $ScriptRoot) "demo-enabled.flag")
}

function Get-HookLogsDirectory {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptRoot
    )

    return (Join-Path (Get-HookRoot -ScriptRoot $ScriptRoot) "logs")
}

function Test-DemoHooksEnabled {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptRoot
    )

    $envEnabled = ""
    if ($null -ne $env:COPILOT_DEMO_HOOKS) {
        $envEnabled = $env:COPILOT_DEMO_HOOKS.ToLowerInvariant()
    }

    if ($envEnabled -in @("1", "true", "yes", "on")) {
        return $true
    }

    return Test-Path (Get-HookFlagPath -ScriptRoot $ScriptRoot)
}

function Convert-HookValueToText {
    param($Value)

    if ($null -eq $Value) {
        return ""
    }

    if ($Value -is [string]) {
        return $Value
    }

    return ($Value | ConvertTo-Json -Compress -Depth 10)
}
