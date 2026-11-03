# Sheet-Test Labs — how they work

Entry point for anyone (human or agent) picking up a character lab. Read
this once before touching a lab; you should not need to reverse-engineer
the scripts.

- **Wording + experiment rules:** `../../PROMPT-RULES.md` (distilled from
  14 Shade batches — these override generic prompt advice).
- **Batch history and verdicts:** each lab's own `README.md` — the
  authoritative record of what was tried and what the human decided.
- **Design context:** `../../docs/superpowers/specs/2026-11-01-sheet-test-design.md`.

## What a lab is

A lab iterates ONE character's prompt wording under controlled conditions:
same frame, same seeds, one wording variable per batch (PROMPT-RULES #7).
Labs exist per character: `shade-lab/`, `keechwah-lab/`, `gulgrim-lab/`, …

## Lab anatomy

| File | Role |
|---|---|
| `descriptions.md` | Single authored block: `## Name (slug)` + prompt text + `Sources:`. **Must** include a `https://www.dndbeyond.com/species/…` URL (build fails without it), `character-bible/Sheets/<Name>.pdf`, and `bible.md locked chunks (main checkout)`; also add `character-bible/approved_<slug>_reference.png` when an approved reference exists, so every verdict has a look to judge against. |
| `prompts.json` | Always the LATEST batch, generated — never hand-edit. |
| `img/` | Latest batch's PNGs (1344×768), downloaded by the runner. |
| `README.md` | Batch history table + verdicts (append-only). |
| `batches/batch<N>/` | Snapshot of `prompts.json` + `descriptions.md` + `img/` taken **as part of every run**, right after the verify gate and before the verdict — never gated on the verdict, never overwritten (PROMPT-RULES #11). No snapshot script exists; copy the three items manually. This folder is what makes batch-to-batch comparison possible. |
| `../../tests/test_<slug>lab.py` | Pins the current block text, key/seed ladder, prompt composition, and workflow family. Updated every batch. |

## Batch lifecycle

```powershell
# 1. Edit ONE wording variable in <lab>/descriptions.md (batch 1 = Arm B block verbatim)

# 2. Build prompts -> <lab>/prompts.json  (--keys is REQUIRED for non-shade slugs:
#    build_lab.py's defaults are shade_s<i>)
python scripts/build_lab.py --descriptions character-bible/sheet-test/<slug>-lab/descriptions.md --out-dir character-bible/sheet-test/<slug>-lab --model-path "C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors" --slug <slug> --seeds 424242 424243 777001 424244 --keys <slug>_g01 <slug>_g02 <slug>_g03 <slug>_g04

# 3. Build one workflow JSON per entry -> workflows/<slug>lab_<key>.json
python scripts/build_sheet_workflows.py --base workflows/base_flux3.json --prompts character-bible/sheet-test/<slug>-lab/prompts.json --out-dir workflows --prefix <slug>lab_

# 4. Generate (ComfyUI at 10.13.37.88:8188; downloads img/<key>.png and records outputs)
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_sheettest.ps1 -Host 10.13.37.88 -Port 8188 -PromptsPath character-bible/sheet-test/<slug>-lab/prompts.json -ImgDir character-bible/sheet-test/<slug>-lab/img -WorkflowPrefix <slug>lab_

# 5. Completion gate: COMPLETE only if every roster PNG exists at 1344x768
python scripts/verify_sheettest.py --prompts character-bible/sheet-test/<slug>-lab/prompts.json --img character-bible/sheet-test/<slug>-lab/img --roster <slug>_g01 <slug>_g02 <slug>_g03 <slug>_g04

# 6. Tests (from repo root; run after every build/wording change).
#    Modules only — discovery does NOT work here (tests/ has no __init__.py),
#    so list them explicitly:
python -m unittest tests.test_<slug>lab tests.test_arm_c tests.test_build_sheet_workflows

# 7. SNAPSHOT NOW — before any verdict: copy prompts.json + descriptions.md +
#    img/ to <lab>/batches/batch<N>/ (N = the batch number just run). Every run
#    lands in its own batch folder so progress stays comparable; top-level files
#    keep holding the latest for the tooling.
# 8. Human verdict -> append to <lab>/README.md -> update tests/test_<slug>lab.py
#    to pin the new block + ladder -> commit the batch (snapshot + top-level
#    latest + README row + test + workflows in ONE commit, as batch17 did in
#    keechwah-lab)
```

## Conventions

- **Keys/seeds:** batch 1 is a baseline control ladder. Seed `424242`
  reproduces the Arm C image byte-identical (determinism control); the
  rest of the original ladder was `424243, 777001, 314159` — Shade
  retired `314159` as a hostile seed, Keechwah replaced it with `424244`.
  Keechwah keys: `keechwah_k01..k04`; surveys: `keechwah_r01..r20`.
  Shade keys: `shade_s0..s3`; surveys: `shade_q01..q20`. Keep each lab's
  prefix scheme stable.
- **20-seed surveys** measure hit rate on frozen wording (4-seed batches
  miss keepers — PROMPT-RULES #10). The 20 seeds come from a recorded
  master seed list, verified disjoint from every prior ladder; the list
  lives as constants in the lab's test file.
- **Workflow files are ephemeral:** only the latest batch's `<slug>lab_*`
  set lives in `workflows/`; older batches are recoverable from git
  history at their batch commit.
- **Frame/addendum are infrastructure** (`FRAME_C`/`ADDENDUM` in
  `scripts/build_arm_b.py`) — never change them inside a wording batch
  (PROMPT-RULES, standing decisions).
- **Locked chunks** in `descriptions.md` stay verbatim unless the human
  approves a deviation (PROMPT-RULES #12).

## Current labs

| Lab | State (see its README for detail) |
|---|---|
| `shade-lab` | Done — 14 batches; batch-13/14 block pinned; approved seeds 777001 + batch-14 keepers. |
| `keechwah-lab` | Batch 17 done; batch 18 (20-seed purple-hold survey) in flight as of 2026-11-02. |
| `gulgrim-lab` | Batch 1 built and ready to run (Arm B baseline, keys `gulgrim_g01–g04`) as of 2026-11-02; generation pending GPU availability. |
