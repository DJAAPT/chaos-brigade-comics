# Arm B Round 2 — Merged-Description Prompts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (preserved Native method) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate six Arm B reference images whose prompts are the merged descriptions (sheet facts + official species canon + locked-chunk wins + round-2 composition rules), byte-identical rig to round 1, so `img/` vs `arm_b/img/` isolates prompt quality alone.

**Architecture:** One authored markdown file (`arm_b/descriptions.md`) is the single source of merged wording — authored by the agent reading the locked bible directly, never by script. A small builder turns it into `arm_b/prompts.json` (round-1's nine-key schema, `arm: "B"`); the existing workflow builder gains a filename-prefix parameter (round-1 defaults unchanged); the existing runner gains path parameters (round-1 defaults unchanged). Round-1 artifacts are never written.

**Tech Stack:** Python 3.14 stdlib + existing `pypdf`/`bs4` tooling, unittest, PowerShell runner, Flux3 Klein via LAN ComfyUI — all inherited from round 1.

**Spec:** `docs/superpowers/specs/2026-11-01-sheet-test-design.md` — "Arm B — Round 2 directive" section is binding for this plan.

## Global Constraints

- Round-1 artifacts are FROZEN: `character-bible/sheet-test/{prompts.json, sheet-bible.md, img/, data/}` and `workflows/sheettest_<slug>.json` are never modified by any task (verify via `git diff --stat` at the end).
- Frame, verbatim, first in every prompt: `solo full-body portrait of a single character, plain background`
- Composition addendum, verbatim, second in every prompt: `standing neutral pose, both arms clearly visible, no shield, nothing held across the body`
- Fixed seed `424242`; base graph `workflows/base_flux3.json`; model `flux3-image-klein-nvfp4.safetensors` — identical to round 1 (prompt is the only variable).
- No `scripts/*.py` may contain the tokens `bible.md`, `refs/`, or `gallery` — merged wins reach prompts ONLY through the authored `descriptions.md` (test_no_local_reference_reads keeps enforcing this).
- No `shield` (case-insensitive) may appear in any Arm B prompt; every Arm B prompt must match `(?i)exactly two arms`; Shade's must match `(?i)adult` and `(?i)not a child`; Keechwah's must match `(?i)no wings`.
- Drop-list mechanics stay out (reuse round-1 `MECHANICS_RE` semantics: named terms + `word +N`; enchanted item names like `Plate, +2` allowed).
- Roster: the same six slugs (chip, gulgrim, keechwah, rocketcandy, shade, vadania). Outputs land in `character-bible/sheet-test/arm_b/img/<slug>.png`, 1344x768.
- Never commit API keys; no `.gitignore` changes; commits to branch `sheet-test` only.

## Review Focus

1. **Authored blocks carrying the very defects round 1 had** (a shield word, toddler-vague Shade, missing wings ban) — pinned by `test_arm_b.py::test_composition_and_win_phrases` (shield-absent, adult/not-a-child, no-wings, exactly-two-arms assertions over all six built prompts).
2. **Round-1 artifacts mutated by round-2 tooling** (runner/builder defaults changed under the old paths) — pinned by `test_arm_b.py::test_round1_defaults_untouched` (builders run with defaults in temp dirs produce byte-identical round-1 outputs) plus a final `git diff --stat` verification step.
3. **Prompts.json schema drift** (nine keys / arm "B" / seed / frame order) — pinned by `test_arm_b.py::test_prompts_schema`.
4. **Sources mis-attributed** (a block crediting the wrong species URL) — pinned by `test_arm_b.py::test_sources_match_blocks` (each entry's species_sources equals the URL written in that block's Sources line).
5. **Workflow-prefix regression** (round-1 graphs renamed or re-prefixed) — pinned by `test_build_sheet_workflows.py::test_default_prefix_round1_unchanged` (new test; default behavior still emits `sheettest_<slug>.json` + `sheettest_<slug>` prefixes).

---

### Task 1: Author the six merged descriptions

**Files:**
- Create: `character-bible/sheet-test/arm_b/descriptions.md`
- Test: `tests/test_arm_b.py` (structure + content pins for this task)

**Interfaces:**
- Consumes (by the agent, directly, not by code): current `O:\Scripts\chaos-brigade-comics\character-bible\bible.md` (main checkout, uncommitted current version), `character-bible/sheet-test/data/sheets.json`, `character-bible/sheet-test/data/species.json`.
- Produces: `descriptions.md` — six blocks:
  `## <Name> (<slug>)` / blank / the merged description paragraph / blank / `Sources:` / `- character-bible/Sheets/<Slug>.pdf` / `- <species url>` / `- bible.md locked chunks (main checkout)` / blank.
  Each block is one self-contained paragraph: sheet facts + species canon + locked-chunk wins + the round-2 composition intent (adult proportions where relevant), containing NO occluding-gear mention (no shield), carrying `exactly two arms` (all six are humanoids), Shade carrying `small adult ... NOT a child`, Keechwah carrying `NO wings`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_arm_b.py (unittest) — descriptions structure/content
# test_six_blocks_with_sources: file exists; six "## " sections matching
#   the six slugs; every block has a Sources block containing its Sheets PDF,
#   a https://www.dndbeyond.com/species/ URL, and the locked-chunks line
# test_no_shield_in_descriptions: "shield" (case-insens) absent from every block
# test_win_phrases: shade block matches (?i)adult and (?i)not a child;
#   keechwah block matches (?i)no wings; all six match (?i)exactly two arms
# test_no_mechanics: round-1 MECHANICS_RE finds nothing in any block
```

- [ ] **Step 2: Run test to verify it FAILS** — `python -m unittest tests.test_arm_b -v` → FAIL (file missing).

- [ ] **Step 3: Author `descriptions.md`** — read the current main-checkout `bible.md` first for verbatim wins (never paraphrase locked chunks), then compose one block per character from the three inputs; keep each block 40–110 words, visual-only (no scores, no history dumps); Rocketcandy excludes the Shield while keeping plate/cape/crest/signet/holy symbol/battleaxe-at-hip; Chip keeps `holding wooden staff (HE holds it)` semantics; Vadania `male ... NOT female` win included; Gulgrim `broad long white beard, frost-covered boots`.

- [ ] **Step 4: Run test to verify it PASSES** — `python -m unittest tests.test_arm_b -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add character-bible/sheet-test/arm_b/descriptions.md tests/test_arm_b.py
git commit -m "sheet-test: author Arm B merged descriptions with round-2 composition rules"
```

---

### Task 2: Build Arm B prompts and workflows

**Files:**
- Create: `scripts/build_arm_b.py`
- Create: `character-bible/sheet-test/arm_b/prompts.json`
- Modify: `scripts/build_sheet_workflows.py` (add `--prefix`, default = round-1 behavior)
- Create: `workflows/sheettest_b_<slug>.json` ×6 (`SaveImage` prefix `sheettest_b_<slug>`)
- Test: extend `tests/test_arm_b.py`; extend `tests/test_build_sheet_workflows.py`

**Interfaces:**
- Consumes: `arm_b/descriptions.md` (Task 1 format), `workflows/base_flux3.json` sentinel contract (round 1), frame/addendum/seed from Global Constraints.
- Produces: `arm_b/prompts.json` — same nine keys as round 1, `arm: "B"`, `prompt = frame + " " + addendum + " " + block`, `species_sources = {page_slug: url}` parsed from the block's Sources line, `workflow: "workflows/base_flux3.json"`, `output: null`. Workflows via `python scripts/build_sheet_workflows.py --base workflows/base_flux3.json --prompts character-bible/sheet-test/arm_b/prompts.json --out-dir workflows --slug-prefix sheettest_b_` where `SaveImage.filename_prefix = <file stem>`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_arm_b.py additions (prompts.json)
# test_prompts_schema: 6 entries == six slugs; exact nine keys in order;
#   arm "B"; seed 424242; frame exact first sentence; prompt starts with
#   frame + " " + addendum; output is None; workflow == workflows/base_flux3.json
# test_composition_and_win_phrases: for all six built prompts — no (?i)shield;
#   matches (?i)exactly two arms; mechanics RE finds nothing;
#   shade matches (?i)adult and (?i)not a child; keechwah matches (?i)no wings
# test_sources_match_blocks: entry species_sources value == the species URL
#   in that block's Sources line of descriptions.md
# tests/test_build_sheet_workflows.py addition:
# test_default_prefix_round1_unchanged: with defaults, output filenames and
#   SaveImage prefixes are sheettest_<slug> (round-1 shape), byte-comparable
```

- [ ] **Step 2: Run tests to verify they FAIL** — `python -m unittest tests.test_arm_b tests.test_build_sheet_workflows -v` → FAIL (prompts.json missing; round-1 test still passes — expected, it pins existing behavior).

- [ ] **Step 3: Implement** — `scripts/build_arm_b.py` CLI:
  `python scripts/build_arm_b.py --descriptions character-bible/sheet-test/arm_b/descriptions.md --out-dir character-bible/sheet-test/arm_b --model-path "C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors"`
  Parse blocks (heading regex `^## (.+) \((\w+)\)$`, paragraph, Sources lines); assemble prompts; `model_hashes` same computation as round 1 (sha256 streamed); write `prompts.json`. Never reads anything but `--descriptions`.
  `build_sheet_workflows.py`: add `--prefix` (default `sheettest_`) and derive `filename_prefix` from the output file stem (so `sheettest_b_shade.json` → `sheettest_b_shade`); keep `slug in filename = prefix + slug + ".json"`.

- [ ] **Step 4: Run tests to verify they PASS**, then generate workflows:
  `python scripts/build_arm_b.py --descriptions character-bible/sheet-test/arm_b/descriptions.md --out-dir character-bible/sheet-test/arm_b --model-path "C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors"`
  `python scripts/build_sheet_workflows.py --base workflows/base_flux3.json --prompts character-bible/sheet-test/arm_b/prompts.json --out-dir workflows --prefix sheettest_b_`
  Full: `python -m unittest discover -s tests -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_arm_b.py scripts/build_sheet_workflows.py character-bible/sheet-test/arm_b/prompts.json workflows/sheettest_b_*.json tests/test_arm_b.py tests/test_build_sheet_workflows.py
git commit -m "sheet-test: build Arm B prompts and prefixed workflows"
```

---

### Task 3: Run the six Arm B generations

**Files:**
- Modify: `scripts/run_sheettest.ps1` (add `-PromptsPath`, `-ImgDir`, `-WorkflowPrefix` — defaults identical to round-1 behavior)
- Create: `character-bible/sheet-test/arm_b/img/<slug>.png` ×6
- Modify: `character-bible/sheet-test/arm_b/prompts.json` (outputs recorded)

**Interfaces:**
- Consumes: `workflows/sheettest_b_<slug>.json`, ComfyUI HTTP API, `arm_b/prompts.json`.
- Produces: six PNGs at `arm_b/img/<slug>.png` (1344x768), Arm B outputs recorded.

- [ ] **Step 1: Parameterize the runner** — three parameters with round-1 defaults; workflow file name = `-WorkflowPrefix + slug + ".json"`; record via `record_output.py --prompts $PromptsPath --output "img/<slug>.png"`; VRAM precheck and exit-1-on-failure behavior unchanged.

- [ ] **Step 2: Sanity that round-1 defaults are untouched** — `git diff scripts/run_sheettest.ps1` shows only additive parameters; run `pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_sheettest.ps1 -WhatIf`-style dry check is NOT available → instead: `powershell` parse check:
  `pwsh -NoProfile -Command "[scriptblock]::Create((Get-Content -Raw .\scripts\run_sheettest.ps1)) | Out-Null; 'parse ok'"` → `parse ok`.

- [ ] **Step 3: Live run (background, observable)**

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_sheettest.ps1 -Host 10.13.37.88 -Port 8188 -PromptsPath character-bible/sheet-test/arm_b/prompts.json -ImgDir character-bible/sheet-test/arm_b/img -WorkflowPrefix sheettest_b_
```
Expected: `ALL SIX GENERATED`, exit 0 (notification arrives when finished).

- [ ] **Step 4: Verify completion**

```powershell
python scripts/verify_sheettest.py --prompts character-bible/sheet-test/arm_b/prompts.json --img character-bible/sheet-test/arm_b/img
python -m unittest discover -s tests -v
```
Expected: `COMPLETE` exit 0; full suite PASS.

- [ ] **Step 5: Round-1 freeze check** — `git diff --stat 5d3ca6d..HEAD -- character-bible/sheet-test/img character-bible/sheet-test/prompts.json character-bible/sheet-test/sheet-bible.md workflows/sheettest_chip.json` → no round-1 file modified (only arm_b/ and scripts/ appear in the working diff). Any round-1 change = stop and report.

- [ ] **Step 6: Commit**

```bash
git add scripts/run_sheettest.ps1 character-bible/sheet-test/arm_b/img character-bible/sheet-test/arm_b/prompts.json
git commit -m "sheet-test: generate six Arm B merged-description images"
```

---

## Handoff to the human

Report the twelve image paths (round 1 `img/` vs round 2 `arm_b/img/`) for side-by-side judgment in `NOTES.md` (human's file). Round-1 freeze reconfirmed; branch `sheet-test` remains unmerged per human instruction.
