# Arm C Round 3 — Full-Body Framing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (preserved Native method) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Six Arm C reference images that differ from Arm B by exactly one clause — a head-to-toe, fixed-distance framing frame — so `arm_b/img/` vs `arm_c/img/` isolates framing alone.

**Architecture:** `build_arm_b.py` gains a `--frame` parameter (default = Arm B's frame, byte-identical round-2 behavior). Arm C prompts are built from `arm_b/descriptions.md` itself (blocks never re-authored) with the new frame; workflows reuse the existing `--prefix` parameter (`sheettest_c_`); the runner's existing path parameters drive generation into `arm_c/`.

**Tech Stack:** inherited unchanged (Python stdlib + unittest, PowerShell runner, Flux3 Klein via LAN ComfyUI).

**Spec:** `docs/superpowers/specs/2026-11-01-sheet-test-design.md` — "Arm C — Round 3 directive" section is binding.

## Global Constraints

- New frame, verbatim (the ONLY change vs Arm B): `solo full-body portrait of a single character, head-to-toe full body with feet visible and empty space above the head, stationary camera at a fixed distance, plain background`
- Arm B frame `solo full-body portrait of a single character, plain background` must remain a byte-prefix of the Arm C frame (the inserted clause is the experiment).
- Addendum, blocks, seed `424242`, base graph, model, roster: byte-identical to Arm B — blocks are read from `character-bible/sheet-test/arm_b/descriptions.md`, never re-authored.
- Defaults stay round-2 behavior: `build_arm_b.py` without `--frame` must produce Arm B prompts identical modulo timestamp; `build_sheet_workflows.py` and `run_sheettest.ps1` need no changes at all.
- Arms A (`img/`) and B (`arm_b/`) are never written by round 3 — verified by freeze checks.
- `prompts.json` schema: same nine keys, `arm: "C"`, outputs recorded as `img/<slug>.png` under `arm_c/`.
- No `scripts/*.py` may contain `bible.md`, `refs/`, or `gallery` tokens (existing guard keeps enforcing).

## Review Focus

1. **Frame wording drift** (typo/reorder in the pinned frame clause) — pinned by `test_arm_c.py::test_frame_clause_exact` (exact string + byte-prefix relationship) and `::test_prompt_is_exact_composition`.
2. **Blocks diverging from Arm B** (re-authoring instead of reuse) — pinned by `::test_blocks_identical_to_arm_b` (strip both frames; remainder must be byte-equal across arms).
3. **Round-2 default regression** — pinned by `::test_default_build_matches_arm_b` (builder run without `--frame` into a temp dir, entries compared to committed `arm_b/prompts.json` with only `timestamp` exempt).
4. **Arm A/B mutation** — freeze checks: `git diff` over `img/`, `arm_b/`, `sheettest_<slug>.json`, `sheettest_b_*.json` empty for all round-3 commits (verification step + final check).
5. **Workflow-family mixups** — pinned by `test_build_sheet_workflows.py::test_arm_c_family_exactly_six` (`sheettest_c_*` = six, SaveImage prefixes `sheettest_c_<slug>`).

---

### Task 1: Parameterize the frame and build Arm C prompts + workflows

**Files:**
- Modify: `scripts/build_arm_b.py` (`--frame` argument, default = Arm B frame; `build_entry(..., frame=FRAME, addendum=ADDENDUM)` plumbing)
- Create: `character-bible/sheet-test/arm_c/prompts.json`
- Create: `workflows/sheettest_c_<slug>.json` ×6 (via existing `--prefix sheettest_c_`)
- Test: `tests/test_arm_c.py` (new), `tests/test_build_sheet_workflows.py` (C-family test)

**Interfaces:**
- Consumes: `arm_b/descriptions.md` (Task 1 of round 2 — unchanged), `workflows/base_flux3.json`, `--prefix` (round 2).
- Produces: `arm_c/prompts.json` (`arm: "C"`, `prompt = FRAME_C + " " + addendum + " " + block`, `output: null`); six `workflows/sheettest_c_<slug>.json` with `SaveImage.filename_prefix = sheettest_c_<slug>`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_arm_c.py (unittest)
# FRAME_C = the pinned frame; FRAME_B imported from test_arm_b conventions
# test_frame_clause_exact: FRAME_C exact string; FRAME_B is byte-prefix of FRAME_C;
#   the inserted middle clause equals the spec's pinned words
# test_prompts_schema: after build — six slugs, nine keys, arm "C", seed 424242,
#   frame key == FRAME_C, prompt starts FRAME_C + " " + addendum, output is None,
#   workflow == workflows/base_flux3.json
# test_blocks_identical_to_arm_b: prompt_c minus FRAME_C == prompt_b minus FRAME_B
#   for all six (byte-equal remainder) — single-variable proof
# test_default_build_matches_arm_b: subprocess build_arm_b WITHOUT --frame into a
#   temp dir; every entry equals committed arm_b/prompts.json except "timestamp"
# tests/test_build_sheet_workflows.py:
# test_arm_c_family_exactly_six: sheettest_c_* == six slugs; and one graph's
#   SaveImage prefix == sheettest_c_<slug>
```

- [ ] **Step 2: Run tests to verify they FAIL** — `python -m unittest tests.test_arm_c tests.test_build_sheet_workflows -v` → FAIL (no `--frame` support; `arm_c/prompts.json` missing; C-family missing).

- [ ] **Step 3: Implement `--frame`** — `build_arm_b.py`: `parser.add_argument("--frame", default=FRAME)` and `build_entry(slug, block, model_hashes, timestamp, frame=FRAME)` using `frame` in the prompt assembly; everything else untouched.

- [ ] **Step 4: Build Arm C artifacts**

```bash
python scripts/build_arm_b.py --descriptions character-bible/sheet-test/arm_b/descriptions.md --out-dir character-bible/sheet-test/arm_c --model-path "C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors" --frame "solo full-body portrait of a single character, head-to-toe full body with feet visible and empty space above the head, stationary camera at a fixed distance, plain background" --arm C
python scripts/build_sheet_workflows.py --base workflows/base_flux3.json --prompts character-bible/sheet-test/arm_c/prompts.json --out-dir workflows --prefix sheettest_c_
python -m unittest discover -s tests -v   # full suite PASS
```

- [ ] **Step 5: Commit**

```bash
git add scripts/build_arm_b.py character-bible/sheet-test/arm_c/prompts.json workflows/sheettest_c_*.json tests/test_arm_c.py tests/test_build_sheet_workflows.py
git commit -m "sheet-test: build Arm C framing-only prompts and workflows"
```

---

### Task 2: Generate the six Arm C images and verify

**Files:**
- Create: `character-bible/sheet-test/arm_c/img/<slug>.png` ×6
- Modify: `character-bible/sheet-test/arm_c/prompts.json` (outputs recorded)

**Interfaces:**
- Consumes: `workflows/sheettest_c_<slug>.json`, runner parameters (round 2), ComfyUI HTTP API.
- Produces: six PNGs at `arm_c/img/<slug>.png`, 1344x768, recorded.

- [ ] **Step 1: Live run (background)**

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_sheettest.ps1 -Host 10.13.37.88 -Port 8188 -PromptsPath character-bible/sheet-test/arm_c/prompts.json -ImgDir character-bible/sheet-test/arm_c/img -WorkflowPrefix sheettest_c_
```
Expected: `ALL SIX GENERATED`, exit 0 (notification when finished).

- [ ] **Step 2: Verify completion + freeze**

```powershell
python scripts/verify_sheettest.py --prompts character-bible/sheet-test/arm_c/prompts.json --img character-bible/sheet-test/arm_c/img
python -m unittest discover -s tests -v
git diff --stat <round-3-base>..HEAD -- character-bible/sheet-test/img character-bible/sheet-test/arm_b workflows/sheettest_chip.json workflows/sheettest_b_chip.json
```
Expected: `COMPLETE` exit 0; suite PASS; freeze diff empty (arms A and B untouched); working tree shows only arm_c/ changes.

- [ ] **Step 3: Commit**

```bash
git add character-bible/sheet-test/arm_c/img character-bible/sheet-test/arm_c/prompts.json
git commit -m "sheet-test: generate six Arm C full-body framing images"
```

---

## Handoff to the human

Report all three arms side by side: `img/` (A: sheets only), `arm_b/img/` (B: merged descriptions), `arm_c/img/` (C: full-body fixed-distance framing) — human judgment recorded in `NOTES.md`. If Arm C's size cues read too weakly, the reserved Arm C-2 (constant door ruler) is the declared follow-up. Branch stays unmerged per human instruction.
