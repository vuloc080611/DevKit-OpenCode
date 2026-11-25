<#
.SYNOPSIS
    Install devkit-opencode skills, custom slash commands, AGENTS.md, and opencode.jsonc.

.DESCRIPTION
    Supports Global (~/.config/opencode) or Project (.opencode/ + root config) installation,
    optional core-only mode (9 core discipline skills), and automatic backup of existing
    AGENTS.md / opencode.jsonc files before overwriting.
#>
[CmdletBinding()]
param(
    [ValidateSet("Global", "Project")]
    [string]$Scope = "Global",

    [string]$ProjectDir = (Get-Location).Path,

    [string]$TargetDir = "",

    [switch]$CoreOnly,

    [switch]$SkipConfig,

    [switch]$NoCommands
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$CoreSkills = @(
    "grill-me",
    "project-planner",
    "systematic-debugging",
    "verification-before-done",
    "tdd-workflow",
    "code-review",
    "security-review",
    "git-commit",
    "readme-generator"
)

if (-not [string]::IsNullOrWhiteSpace($TargetDir)) {
    $SkillsDest = Join-Path $TargetDir "skills"
    $CommandsDest = Join-Path $TargetDir "commands"
    $ConfigRoot = $TargetDir
} elseif ($Scope -eq "Project") {
    $SkillsDest = Join-Path $ProjectDir ".opencode\skills"
    $CommandsDest = Join-Path $ProjectDir ".opencode\commands"
    $ConfigRoot = $ProjectDir
} else {
    $BaseGlobal = Join-Path $env:USERPROFILE ".config\opencode"
    $SkillsDest = Join-Path $BaseGlobal "skills"
    $CommandsDest = Join-Path $BaseGlobal "commands"
    $ConfigRoot = $BaseGlobal
}

function Copy-WithBackup {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )
    if (Test-Path $Destination) {
        $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $BackupPath = "$Destination.bak.$Stamp"
        Copy-Item -Force $Destination $BackupPath
        Write-Host "[backup] $Destination -> $BackupPath"
    }
    Copy-Item -Force $Source $Destination
    Write-Host "[copy]   $Destination"
}

New-Item -ItemType Directory -Force $SkillsDest | Out-Null

$SkillCount = 0
if ($CoreOnly) {
    foreach ($Skill in $CoreSkills) {
        $Src = Join-Path $RepoRoot "skills\$Skill"
        $Dst = Join-Path $SkillsDest $Skill
        if (Test-Path $Dst) { Remove-Item -Recurse -Force $Dst }
        Copy-Item -Recurse -Force $Src $Dst
        $SkillCount++
    }
} else {
    Get-ChildItem -Directory (Join-Path $RepoRoot "skills") | ForEach-Object {
        $Dst = Join-Path $SkillsDest $_.Name
        if (Test-Path $Dst) { Remove-Item -Recurse -Force $Dst }
        Copy-Item -Recurse -Force $_.FullName $Dst
        $SkillCount++
    }
}
Write-Host "[skills] Installed $SkillCount skill(s) into $SkillsDest"

$CmdCount = 0
$CommandsSource = Join-Path $RepoRoot "commands"
if (-not $NoCommands -and (Test-Path $CommandsSource)) {
    New-Item -ItemType Directory -Force $CommandsDest | Out-Null
    Get-ChildItem -File -Filter "*.md" $CommandsSource | ForEach-Object {
        Copy-Item -Force $_.FullName (Join-Path $CommandsDest $_.Name)
        $CmdCount++
    }
    Write-Host "[cmds]   Installed $CmdCount slash command(s) into $CommandsDest"
}

if (-not $SkipConfig) {
    New-Item -ItemType Directory -Force $ConfigRoot | Out-Null
    Copy-WithBackup -Source (Join-Path $RepoRoot "AGENTS.md") -Destination (Join-Path $ConfigRoot "AGENTS.md")
    Copy-WithBackup -Source (Join-Path $RepoRoot "config\opencode.jsonc.example") -Destination (Join-Path $ConfigRoot "opencode.jsonc")
}

Write-Host "Done! Launch OpenCode and verify with /verify or ask which skills are loaded."
