# Run the six sheet-test Flux3 generations against ComfyUI and record outputs.
# Any failure prints FAILED <slug>: <reason> and exits 1 — no silent partials.
[CmdletBinding()]
param(
    [Alias('Host')]
    [string]$HostName = '10.13.37.88',
    [int]$Port = 8188,
    [int]$TimeoutSec = 300,
    [string]$PromptsPath = 'character-bible/sheet-test/prompts.json',
    [string]$ImgDir = 'character-bible/sheet-test/img',
    [string]$WorkflowPrefix = 'sheettest_'
)

$ErrorActionPreference = 'Stop'
$base = "http://${HostName}:${Port}"
$wfDir = 'workflows'

$slugs = ((Get-Content $promptsPath -Raw | ConvertFrom-Json).PSObject.Properties.Name) | Sort-Object
if ($slugs.Count -ne 6) {
    Write-Host "FAILED setup: expected 6 characters in prompts.json, found $($slugs.Count)"
    exit 1
}

# Soft VRAM precheck
try {
    $stats = Invoke-RestMethod "$base/system_stats" -TimeoutSec 15
    $dev = $stats.devices | Select-Object -First 1
    $freeGb = [math]::Round($dev.vram_free / 1GB, 2)
    $totalGb = [math]::Round($dev.vram_total / 1GB, 2)
    Write-Host "GPU: $($dev.name) — VRAM free $freeGb / $totalGb GB"
    if ($dev.vram_free -lt 4GB) { Write-Warning 'VRAM free below 4 GB — generation may fail or page' }
} catch {
    Write-Warning "system_stats unavailable: $($_.Exception.Message)"
}

New-Item -ItemType Directory -Force -Path $imgDir | Out-Null

foreach ($slug in $slugs) {
    $wfPath = Join-Path $wfDir "$WorkflowPrefix$slug.json"
    if (-not (Test-Path $wfPath)) { Write-Host "FAILED ${slug}: missing $wfPath"; exit 1 }
    $graph = Get-Content $wfPath -Raw | ConvertFrom-Json
    $body = @{ prompt = $graph; client_id = "sheet-test-$slug" } | ConvertTo-Json -Depth 64

    Write-Host "[$slug] submitting..."
    try {
        $resp = Invoke-RestMethod -Method Post -Uri "$base/prompt" -Body $body -ContentType 'application/json' -TimeoutSec 30
    } catch {
        Write-Host "FAILED ${slug}: POST /prompt — $($_.Exception.Message)"
        exit 1
    }
    if ($resp.node_errors -and ($resp.node_errors.PSObject.Properties.Name.Count -gt 0)) {
        Write-Host "FAILED ${slug}: node errors: $($resp.node_errors | ConvertTo-Json -Depth 8)"
        exit 1
    }
    $jobId = $resp.prompt_id
    Write-Host "[$slug] queued as $jobId — waiting (timeout ${TimeoutSec}s)..."

    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    $entry = $null
    while ((Get-Date) -lt $deadline) {
        try { $hist = Invoke-RestMethod "$base/history/$jobId" -TimeoutSec 15 } catch { $hist = $null }
        if ($hist -and $hist.PSObject.Properties.Name -contains $jobId) { $entry = $hist.$jobId; break }
        Start-Sleep -Seconds 5
    }
    if (-not $entry) { Write-Host "FAILED ${slug}: history timeout after ${TimeoutSec}s"; exit 1 }

    $imgList = $null
    if ($entry.outputs) {
        $firstOut = $entry.outputs.PSObject.Properties | Select-Object -First 1
        if ($firstOut) { $imgList = $firstOut.Value.images }
    }
    if (-not $imgList -or $imgList.Count -eq 0) {
        $status = $entry.status.status_str
        $msgs = if ($entry.status.messages) { ($entry.status.messages | ConvertTo-Json -Depth 8) } else { 'none' }
        Write-Host "FAILED ${slug}: no outputs (status=$status) messages: $msgs"
        exit 1
    }

    $img = $imgList[0]
    $qs = "filename=$([uri]::EscapeDataString([string]$img.filename))&subfolder=$([uri]::EscapeDataString([string]$img.subfolder))&type=$([uri]::EscapeDataString([string]$img.type))"
    try {
        Invoke-WebRequest -Uri "$base/view?$qs" -OutFile (Join-Path $imgDir "$slug.png") -TimeoutSec 60
    } catch {
        Write-Host "FAILED ${slug}: download — $($_.Exception.Message)"
        exit 1
    }

    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    python scripts/record_output.py --prompts $promptsPath --character $slug --output "img/$slug.png" --timestamp $ts
    if ($LASTEXITCODE -ne 0) { Write-Host "FAILED ${slug}: record_output exit $LASTEXITCODE"; exit 1 }
    Write-Host "OK $slug <- $($img.filename)"
}

Write-Host 'ALL SIX GENERATED'
exit 0
