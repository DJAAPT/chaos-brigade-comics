# Flux3-Only Pipeline Switch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Flux3 Image Klein the only generation engine referenced by the comics pipeline — pin the Flux3 base workflow, repoint all process docs, purge the Flux2 workflow artifact.

**Architecture:** One new artifact (`workflows/base_flux3.json`, pinned from the verified text-only graph with a `{{PROMPT}}` sentinel) plus surgical edits to four existing docs. No code, no test runner — verification is PowerShell assertion scripts per task plus one live `validate_workflow` call against the running ComfyUI.

**Tech Stack:** Markdown, JSON workflow graphs (ComfyUI API format), PowerShell test scripts, comfy MCP tools.

**Spec:** `docs/superpowers/specs/2026-11-01-flux3-switch-design.md` (approved 2026-11-01)

## Global Constraints

- Commits go to `main` — standing user consent from this session (same repo, same pattern as the shade-identity-fix plan).
- Rig, copied verbatim from the spec: unet `flux3-image-klein-nvfp4.safetensors` (`weight_dtype: default`), CLIP `qwen3vl_4b_int8_convrot.safetensors` type `flux3`, VAE `flux2-vae.safetensors`, KSampler 15 steps / cfg 1.0 / er_sde / simple, latent 1344×768.
- Sentinel: the populated text node's `inputs.text` becomes exactly `{{PROMPT}}`; every other node byte-identical to `workflows/bibleref_a_origseed.json`.
- The filename `flux2-vae.safetensors` is legitimate everywhere (Flux3 reuses that VAE) — it must survive all edits and all greps.
- Multi-reference stays parked: no `ReferenceMultiLatent` or reference-image nodes added anywhere.
- Only the spec's six changes. README quickstart (stale `comfy.exe` path), Flux2 model files on disk, Flux2-era output PNGs, and all unrelated untracked user files stay untouched — commits stage explicit paths only, never `git add -A`.
- Tests run as workspace scripts (`<workspace>/task-N-test.ps1`) through `task-done`, same pattern as the previous plan.

## Review Focus

Spec-implied failure modes no single task test covers — each is pinned to the task that owns it:

1. **Sentinel contract silently broken** — if the pinned graph's text node isn't exactly `{{PROMPT}}` (or the wrong node was edited), every future template-fill no-ops without error. Pinned by Task 1's deep-compare test: the pinned file equals the source in every field except that one text value.
2. **Graph validates as a file but fails on the live server** (missing model, stale object_info). Pinned by Task 1's live `validate_workflow` step — `valid: true` against `127.0.0.1:8188`, recorded as evidence.
3. **The `flux2-vae` exclusion hides a real leftover** — a filtered grep can pass while prose like "Flux2 Dev" survives. Pinned by Task 4's unfiltered hit-list review: every remaining `flux2`/`Flux 2` hit across README/bible/director/FLUX3-SETUP must be the VAE filename or a FLUX3-SETUP download/VAE-history line.
4. **Deletion hits the wrong file or leaves siblings** — unrecoverable untracked delete. Pinned by Task 3's test: zero files matching `*flux2*` remain in `workflows/`, and the specific path `workflows/flux2_detail_closeup.json` is gone.
5. **Editing bible.md again disturbs the just-locked Shade block** (the shade plan landed days-hours earlier in the same file). Pinned by Task 2's regression test: alongside the Flux2-grep==0, `ASK, DON'T GUESS`==1, `Approved identity ref`==1, and `no gray hair, no white hair`==1 must still hold.

---

### Task 1: Pin `workflows/base_flux3.json`

**Files:**
- Create: `workflows/base_flux3.json`
- Source (read-only): `workflows/bibleref_a_origseed.json`
- Test: workspace `task-1-test.ps1`

**Interfaces:**
- Consumes: nothing
- Produces: `workflows/base_flux3.json` — the pinned Flux3 text-only graph with `{{PROMPT}}` sentinel; Task 2's director edit references this path, Task 4 sweeps it.

- [ ] **Step 1: Write the failing test**

Workspace `task-1-test.ps1`:

```powershell
$src = Get-Content "workflows\bibleref_a_origseed.json" -Raw | ConvertFrom-Json
$pin = Get-Content "workflows\base_flux3.json" -Raw | ConvertFrom-Json   # file missing -> RED
$fail = @()
$u = ($pin.PSObject.Properties | Where-Object { $_.Value.class_type -eq "UNETLoader" }).Value.inputs
if ($u.unet_name -ne "flux3-image-klein-nvfp4.safetensors" -or $u.weight_dtype -ne "default") { $fail += "unet" }
$c = ($pin.PSObject.Properties | Where-Object { $_.Value.class_type -eq "CLIPLoader" }).Value.inputs
if ($c.clip_name -ne "qwen3vl_4b_int8_convrot.safetensors" -or $c.type -ne "flux3") { $fail += "clip" }
$v = ($pin.PSObject.Properties | Where-Object { $_.Value.class_type -eq "VAELoader" }).Value.inputs
if ($v.vae_name -ne "flux2-vae.safetensors") { $fail += "vae" }
$k = ($pin.PSObject.Properties | Where-Object { $_.Value.class_type -eq "KSampler" }).Value.inputs
if ($k.steps -ne 15 -or $k.cfg -ne 1 -or $k.sampler_name -ne "er_sde" -or $k.scheduler -ne "simple") { $fail += "sampler" }
$l = ($pin.PSObject.Properties | Where-Object { $_.Value.class_type -eq "EmptyFlux2LatentImage" }).Value.inputs
if ($l.width -ne 1344 -or $l.height -ne 768) { $fail += "latent" }
$texts = @($pin.PSObject.Properties | Where-Object { $_.Value.class_type -eq "CLIPTextEncode" } | ForEach-Object { $_.Value.inputs.text })
if ((@($texts | Where-Object { $_ -eq "{{PROMPT}}" }).Count) -ne 1) { $fail += "sentinel" }
if ((@($texts | Where-Object { $_ -eq "" }).Count) -ne 1) { $fail += "empty-negative" }
# deep-compare: every field except the one sentinel text must equal source
$srcTexts = @($src.PSObject.Properties | Where-Object { $_.Value.class_type -eq "CLIPTextEncode" } | ForEach-Object { $_.Value.inputs.text })
$srcPopulated = ($src.PSObject.Properties | Where-Object { $_.Value.class_type -eq "CLIPTextEncode" -and $_.Value.inputs.text -ne "" }).Name
foreach ($p in $src.PSObject.Properties) {
  $a = $p.Value | ConvertTo-Json -Depth 20 -Compress
  $b = $pin.($p.Name) | ConvertTo-Json -Depth 20 -Compress
  if ($p.Name -eq $srcPopulated) {
    $a = $a -replace [regex]::Escape(($src.($p.Name).inputs.text | ConvertTo-Json -Compress)), '"__TEXT__"'
    $b = $b -replace [regex]::Escape(($pin.($p.Name).inputs.text | ConvertTo-Json -Compress)), '"__TEXT__"'
  }
  if ($a -ne $b) { $fail += "node $($p.Name) drifted" }
}
if ($fail.Count) { Write-Output "FAIL $($fail -join ',')"; exit 1 }
Write-Output "PASS rig+sentinel+deep-compare ($($src.PSObject.Properties.Count) nodes identical except sentinel)"
```

- [ ] **Step 2: Run test to verify it fails**

Run: workspace `task-1-test.ps1` via `task-done` (or directly first)
Expected: FAIL — `base_flux3.json` not found.

- [ ] **Step 3: Create `workflows/base_flux3.json`**

Copy `workflows/bibleref_a_origseed.json`, then set the **populated** `CLIPTextEncode` node's (the one whose `inputs.text` is non-empty, node id `4`) `inputs.text` to the literal string `{{PROMPT}}`. Change nothing else — not the seed, not `SaveImage`, not the empty negative.

- [ ] **Step 4: Run test to verify it passes**

Run: same script
Expected: PASS — `rig+sentinel+deep-compare (8 nodes identical except sentinel)`.

- [ ] **Step 5: Live-validate the graph**

Call MCP `validate_workflow` with `workflow_path` = `workflows/base_flux3.json` against the running server.
Expected: `{"valid": true, ...}` — record the raw result as evidence. If invalid: fix the pinned file (not the test), re-run Step 4, re-validate.

- [ ] **Step 6: Commit**

```bash
git add workflows/base_flux3.json
git commit -m "workflows: pin Flux3 Klein base workflow with prompt sentinel"
```

---

### Task 2: Repoint process docs at Flux3

**Files:**
- Modify: `README.md:2-3`, `README.md:8`
- Modify: `character-bible/bible.md:7`
- Modify: `scene-director/director.md:37`
- Test: workspace `task-2-test.ps1`

**Interfaces:**
- Consumes: `workflows/base_flux3.json` exists (Task 1) — the path director.md will name.
- Produces: process docs with zero Flux2-engine references; Task 4 re-sweeps them.

- [ ] **Step 1: Write the failing test**

Workspace `task-2-test.ps1`:

```powershell
$docs = @("README.md", "character-bible\bible.md", "scene-director\director.md")
# Flux2 engine references must be gone; lookahead keeps the legit flux2-vae filename
$left = @(Select-String -Path $docs -Pattern "Flux ?2(?!-vae)|base_flux2|fp8mixed|mistral fp8")
# regression guards: this plan edits bible.md again — the shade lock must survive
$ask = @(Select-String -Path "character-bible\bible.md" -Pattern "ASK, DON'T GUESS").Count
$ref = @(Select-String -Path "character-bible\bible.md" -Pattern "Approved identity ref").Count
$sfx = @(Select-String -Path "character-bible\bible.md" -Pattern "no gray hair, no white hair").Count
$dir = @(Select-String -Path "scene-director\director.md" -Pattern "base_flux3\.json").Count
if ($left.Count -eq 0 -and $ask -eq 1 -and $ref -eq 1 -and $sfx -eq 1 -and $dir -eq 1) {
  Write-Output "PASS flux2refs=0 ask=$ask shadeRef=$ref suffix=$sfx director->$dir"; exit 0 }
Write-Output "FAIL flux2refs=$left.Count (lines: $($left.LineNumber -join ',')) ask=$ask ref=$ref sfx=$sfx dir=$dir"; exit 1
```

- [ ] **Step 2: Run test to verify it fails**

Expected: FAIL — `flux2refs` > 0 (README 2/3/8, bible 7, director 37 still Flux2).

- [ ] **Step 3: Make the five edits**

README line 2 → `ComfyUI: http://10.13.37.88:8188 — this machine's LAN IP (http://127.0.0.1:8188 works too) (Flux3 Image Klein nvfp4, 5070 Ti)`

README line 3 → `Base workflow: workflows/base_flux3.json — Flux3 Image Klein text-to-image 1344x768, unet flux3-image-klein-nvfp4, CLIP qwen3vl_4b (type flux3), VAE flux2-vae, 15 steps / cfg 1.0 / er_sde / simple.`

README line 8 → `3. **Flux 3 generation** — \`generate/\` + \`workflows/\` (pinned JSON, seed log)`

bible.md line 7, first sentence only → `Flux 3 (Klein, text-only) has no identity memory between prompts.` (rest of the paragraph unchanged)

director.md line 37 → `3. generate Flux JSONs from bible + plan (reuse \`workflows/base_flux3.json\`)`

- [ ] **Step 4: Run test to verify it passes**

Expected: PASS — `flux2refs=0 ask=1 shadeRef=1 suffix=1 director->1`.

- [ ] **Step 5: Commit**

```bash
git add README.md character-bible/bible.md scene-director/director.md
git commit -m "docs: repoint pipeline docs from Flux2 to Flux3 Klein"
```

---

### Task 3: Purge Flux2 workflow artifact, complete setup doc

**Files:**
- Delete: `workflows/flux2_detail_closeup.json` (untracked — unrecoverable; approved via spec Approach B)
- Modify: `FLUX3-SETUP.md:3-5` (status block), `FLUX3-SETUP.md:103` (the "runs alongside" line)
- Test: workspace `task-3-test.ps1`

**Interfaces:**
- Consumes: nothing
- Produces: no `*flux2*` filename left in `workflows/`; setup doc marked complete.

- [ ] **Step 1: Write the failing test**

Workspace `task-3-test.ps1`:

```powershell
$named = @(Get-ChildItem "workflows" -Filter "*flux2*" -File -ErrorAction SilentlyContinue)
$setup = Get-Content "FLUX3-SETUP.md" -Raw
$complete = $setup -match "Status: COMPLETE \(2026-11-01\)"
$alongside = $setup -match "runs alongside"
if ($named.Count -eq 0 -and $complete -and -not $alongside) {
  Write-Output "PASS flux2WorkflowFiles=0 status=COMPLETE alongsideGone"; exit 0 }
Write-Output "FAIL flux2Files=$($named.Name -join ',') complete=$complete alongside=$alongside"; exit 1
```

- [ ] **Step 2: Run test to verify it fails**

Expected: FAIL — `flux2_detail_closeup.json` still present, status not COMPLETE, "runs alongside" present.

- [ ] **Step 3: Delete the workflow and edit the setup doc**

```powershell
Remove-Item "workflows\flux2_detail_closeup.json"   # unrecoverable, spec-approved
```

FLUX3-SETUP.md lines 3-5 →

```markdown
Status: COMPLETE (2026-11-01). Model files installed; the comics pipeline
now runs Flux3-only (see README) — Flux2 is no longer used for generation.
`flux3` CLIP type and `ReferenceMultiLatent` are confirmed live on `127.0.0.1:8188`.
```

FLUX3-SETUP.md line 103 (`Nothing about your Flux2 setup changes — this runs alongside it.`) →

```markdown
Flux2's setup is retired from the pipeline; files on disk remain but nothing uses them.
```

Everything else in FLUX3-SETUP.md (download checklist, VAE notes) stays — it remains the re-install reference.

- [ ] **Step 4: Run test to verify it passes**

Expected: PASS — `flux2WorkflowFiles=0 status=COMPLETE alongsideGone`.

- [ ] **Step 5: Commit**

```bash
git add FLUX3-SETUP.md
git commit -m "setup: mark Flux3 setup complete, purge Flux2 baseline workflow"
```
(The deleted JSON was untracked — nothing to stage for it; verify with `git status` that no *other* file disappeared.)

---

### Task 4: Final consistency sweep + commit plan docs

**Files:**
- Read-only across README.md, character-bible/bible.md, scene-director/director.md, FLUX3-SETUP.md
- Commit: `docs/superpowers/specs/2026-11-01-flux3-switch-design.md`, `docs/superpowers/plans/2026-11-01-flux3-switch.md`
- Test: workspace `task-4-test.ps1`

**Interfaces:**
- Consumes: Tasks 1-3
- Produces: none (verification only)

- [ ] **Step 1: Write the failing test (re-runs every contract)**

Workspace `task-4-test.ps1`:

```powershell
$docs = @("README.md", "character-bible\bible.md", "scene-director\director.md")
$left = @(Select-String -Path $docs -Pattern "Flux ?2(?!-vae)|base_flux2|fp8mixed|mistral fp8")
$ask = @(Select-String -Path "character-bible\bible.md" -Pattern "ASK, DON'T GUESS").Count
$ref = @(Select-String -Path "character-bible\bible.md" -Pattern "Approved identity ref").Count
$sfx = @(Select-String -Path "character-bible\bible.md" -Pattern "no gray hair, no white hair").Count
$base = Test-Path "workflows\base_flux3.json"
$old = Test-Path "workflows\flux2_detail_closeup.json"
$sent = (Get-Content "workflows\base_flux3.json" -Raw) -match '\{\{PROMPT\}\}'
$setup = (Get-Content "FLUX3-SETUP.md" -Raw) -match "Status: COMPLETE \(2026-11-01\)"
if ($left.Count -eq 0 -and $ask -eq 1 -and $ref -eq 1 -and $sfx -eq 1 -and $base -and -not $old -and $sent -and $setup) {
  Write-Output "PASS flux2refs=0 ask=$ask ref=$ref sfx=$sfx baseFlux3=$base sentinel=$sent setupDone=$setup"; exit 0 }
Write-Output "FAIL flux2refs=$($left.Count) ask=$ask ref=$ref sfx=$sfx base=$base oldGone=$(-not $old) sentinel=$sent setup=$setup"; exit 1
```

- [ ] **Step 2: Run test to verify it fails**

Expected: FAIL while any earlier task is incomplete; PASS once Tasks 1-3 are done (this is the whole-branch gate — if it fails here, one of the earlier tasks' edits did not stick).

- [ ] **Step 3: Unfiltered hit-list review (Review Focus #3)**

```powershell
Select-String -Path README.md, character-bible\bible.md, scene-director\director.md, FLUX3-SETUP.md -Pattern "flux2|Flux 2|Flux2"
```

Read every hit. Expected: each line is either the `flux2-vae.safetensors` filename or a legitimate FLUX3-SETUP download/VAE-history line (e.g. the VAE section, "Flux2-Dev 32B" comparison note, Civitai rename rows). Any other line = a real leftover → fix in the owning file, re-run Step 1, amend the relevant task's commit.

- [ ] **Step 4: Commit plan + spec docs**

```bash
git add docs/superpowers/specs/2026-11-01-flux3-switch-design.md docs/superpowers/plans/2026-11-01-flux3-switch.md
git commit -m "docs: flux3 switch design and implementation plan"
```
