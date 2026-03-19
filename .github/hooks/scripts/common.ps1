$ErrorActionPreference = "Stop"

function Get-HookRoot {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptRoot
    )

    return (Split-Path -Parent $ScriptRoot)
}

function Get-HookLogsDirectory {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptRoot
    )

    return (Join-Path (Get-HookRoot -ScriptRoot $ScriptRoot) "logs")
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
