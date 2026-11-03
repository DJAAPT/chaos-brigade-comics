# Lineup Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove scene-first holds Shade likeness on an empty lineup wall in `character-bible/lineup-lab/` batch 1.

**Architecture:** Empty 1344x768 wall via `base_flux3.json`; Shade inserted via masked `ReferenceMultiLatent` / `VAEEncodeForInpaint` workflow from `approved_shade_reference.png`; lab ledger mirrors `sheet-test` batch pattern with snapshot-before-verdict.

**Tech Stack:** Flux3 Klein nvfp4 + Qwen3-VL-4B + flux2-vae; ComfyUI local 127.0.0.1:8188; python + powershell runner scripts.

**Spec:** `docs/superpowers/specs/2026-11-03-lineup-lab-design.md`

## Global Constraints

- Approved refs only; Shade ref `character-bible/approved_shade_reference.png`.
- Models exactly `flux3-image-klein-nvfp4.safetensors`, `qwen3vl_4b_int8_convrot.safetensors`, `flux2-vae.safetensors`.
- Resolution 1344x768 every image.
- Local free nodes only; no partner-API nodes.
- No height marks in backdrop.
- Never overwrite: top-level `img/` + `prompts.json` are latest; every run snapshots to `batches/batch<N>/` before verdict.

## Review Focus

1. Backdrop with people in it — expect empty wall, no faces; pinned by backdrop workflow prompt check + human eyeball.
2. Wrong Shade face (blond, bald, beard, wrong vest) — expect bible Shade; pinned by ref-image hash check + human cold-recognition.
3. Resolution drift — expect 1344x768; pinned by verify gate.
4. Snapshot missing — expect batch folder with prompts+descriptions+img; pinned by snapshot check.
5. Sheet-test mutation — expect zero diff outside `lineup-lab/` + new `workflows/lineuplab_*`; pinned by freeze diff.

---

### Task 1: Scaffold lineup-lab ledger

**Files:**
- Create: `character-bible/lineup-lab/README.md`
- Create: `character-bible/lineup-lab/descriptions.md`
- Create: `character-bible/lineup-lab/slots.json`
- Create: `character-bible/lineup-lab/prompts.json`
- Create: `tests/test_lineuplab.py`

**Interfaces:**
- Consumes: `character-bible/bible.md` Shade locked chunk; `sheet-test/README.md` batch lifecycle as pattern.
- Produces: `lineup-lab/prompts.json` keys `wall_empty`, `wall_shade_s1`; `slots.json` six slots with heights.

- [ ] **Step 1: Write the failing test**

```python
def test_lineuplab_ledger_exists():
    assert ledger_has_batch_table()
    assert prompts_keys() == ["wall_empty", "wall_shade_s1"]
    assert slots_has_six_with_shade_3ft()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_lineuplab -v`
Expected: FAIL with "lineup-lab not found"

- [ ] **Step 3: Implement ledger files in `character-bible/lineup-lab/`**

README batch table + batch-1 row; descriptions wall prompt (empty neutral lineup wall, no people, no height marks) + Shade insert prompt reusing bible Shade chunk verbatim; slots.json six positions left-to-right with Shade 3ft slot; prompts.json two entries with seeds 424242 wall, 777001 shade, model hashes.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_lineuplab -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add character-bible/lineup-lab tests/test_lineuplab.py docs/superpowers/specs/2026-11-03-lineup-lab-design.md
git commit -m "lineup-lab: scaffold batch-1 ledger"
```

---

### Task 2: Build wall + insert workflows

**Files:**
- Create: `workflows/lineuplab_wall_empty.json`
- Create: `workflows/lineuplab_wall_shade.json`
- Modify: `scripts/build_sheet_workflows.py` only if per-entry seed needed, else new small `scripts/build_lineuplab.py`

**Interfaces:**
- Consumes: `workflows/base_flux3.json` for wall; `workflows/base_flux3_multiref.json` as insert base; Task 1 prompts.json.
- Produces: Two runnable workflow JSONs with SaveImage prefixes matching stems.

- [ ] **Step 1: Write the failing test**

```python
def test_lineuplab_workflows_family():
    assert workflows_exist(["lineuplab_wall_empty", "lineuplab_wall_shade"])
    assert wall_has_no_loadimage_ref()
    assert shade_refs_approved_shade_png()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_lineuplab.TestWorkflows -v`
Expected: FAIL workflows missing

- [ ] **Step 3: Implement `workflows/lineuplab_wall_*.json`**

Wall: copy base_flux3 1344x768, wall prompt, seed 424242. Insert: copy base_multiref, LoadImage `approved_shade_reference.png`, prompt = wall context + bible Shade chunk, seed 777001, denoise to be recorded.

- [ ] **Step 4: Run test + validate workflows**

Run: `python -m unittest tests.test_lineuplab -v`
Expected: PASS; plus Comfy validate both JSONs load.

- [ ] **Step 5: Commit**

```bash
git add workflows/lineuplab_*.json scripts/build_lineuplab.py tests/test_lineuplab.py
git commit -m "lineup-lab: wall and shade-insert workflows"
```

---

### Task 3: Generate batch 1 and snapshot

**Files:**
- Create: `character-bible/lineup-lab/img/wall_empty.png`
- Create: `character-bible/lineup-lab/img/wall_shade_s1.png`
- Create: `character-bible/lineup-lab/batches/batch1/`

**Interfaces:**
- Consumes: Task 2 workflows; ComfyUI at 127.0.0.1:8188.
- Produces: Two 1344x768 PNGs + batch1 snapshot.

- [ ] **Step 1: Generate wall**

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_sheettest.ps1 -Host 127.0.0.1 -Port 8188 -PromptsPath character-bible/lineup-lab/prompts.json -ImgDir character-bible/lineup-lab/img -WorkflowPrefix lineuplab_
```

Expected: both PNGs exist at 1344x768.

- [ ] **Step 2: Verify + snapshot before verdict**

Run: `python scripts/verify_sheettest.py --prompts character-bible/lineup-lab/prompts.json --img character-bible/lineup-lab/img --roster wall_empty wall_shade_s1`
Then copy prompts.json + descriptions.md + img/ to `batches/batch1/`.
Expected: COMPLETE exit 0; batch1 has three items.

- [ ] **Step 3: Commit**

```bash
git add character-bible/lineup-lab/img character-bible/lineup-lab/prompts.json character-bible/lineup-lab/batches/batch1
git commit -m "lineup-lab: batch-1 wall and shade insert"
```

---

## Handoff to the human

Show `lineup-lab/img/wall_empty.png` beside `img/wall_shade_s1.png` and `approved_shade_reference.png` — cold-recognition check on hair, face, vest, stature with no height marks. Verdict in `lineup-lab/README.md`; if Shade holds, batch 2 adds one more character; if not, vary mask/denoise as batch 2.
