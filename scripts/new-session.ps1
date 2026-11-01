#Requires -Version 7
param([Parameter(Mandatory=$true)][string]$SessionId)
# Chaos Brigade auto pipeline v0.1 skeleton
# Usage: .\new-session.ps1 -SessionId 69a905e0416be7e716793df0
$ErrorActionPreference='Stop'
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$SessionFile = "O:\ExternalSites\html\DND\session\$SessionId.json"
$OutDir = Join-Path $ProjectRoot "sessions\$SessionId"
New-Item -ItemType Directory -Force $OutDir | Out-Null
if (!(Test-Path $SessionFile)) { throw "Session not found: $SessionFile" }

# 1. Load transcript, chunk by 10-min marks, score funny/epic/fail/plot
# TODO v0.2: LLM scoring. v0.1: dump transcript excerpt for manual plan.
$j = Get-Content $SessionFile -Raw | ConvertFrom-Json
$transcript = $j.transcript
$transcript | Out-File (Join-Path $OutDir 'transcript.txt')
Write-Host "Transcript saved. Length: $($transcript.Length) chars"
Write-Host 'Next: write plan.json per scene-director/director.md, then generate Flux JSONs from character-bible/bible.md'
Write-Host "Plan template: sessions/<id>/plan.json = [{beat, type, characters[], location, action, panels, narration, quotes[]}]"
# 2. Generate step is manual for now (see README Quickstart). Auto submit coming after S1 comics lock.
