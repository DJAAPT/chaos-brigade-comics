# Sheet-Test Reference Images Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate six new solo character reference images whose prompts are built only from the exported D&D Beyond sheet PDFs plus official DDB species text, logged auditably in `character-bible/sheet-test/`, for side-by-side comparison against the approved gallery-grounded set.

**Architecture:** Six sequential shell-out scripts (Python for extraction/assembly, one PowerShell runner mirroring the README's S1 curl flow) with shared JSON contracts in `character-bible/sheet-test/data/`. An in-repo Flux3 Klein graph (`bibleref_a_origseed.json`) is pinned first as `workflows/base_flux3.json` with a prompt sentinel; everything downstream derives from it. Standard-library `unittest` tests with fixture/offline data for all pure steps; the two live steps (DDB fetch, ComfyUI run) verify by command output.

**Tech Stack:** Python 3.14 (tooling deps, user-site: `pypdf`, `beautifulsoup4`), PowerShell 7 + `curl.exe`, ComfyUI HTTP API (`/prompt`, `/history`, `/view`), Git on `main`.

**Spec:** `docs/superpowers/specs/2026-11-01-sheet-test-design.md` — the plan argues from it; executors read both.

## Global Constraints

- `character-bible/bible.md` is LOCKED: no task reads or writes it. `character-bible/refs/` and `O:\ExternalSites\html\DND\gallery\` are never read by any extraction or prompt-building code.
- Prompt frame, verbatim, first in every prompt: `solo full-body portrait of a single character, plain background`
- No global anti-drift suffix in any prompt (spec decision).
- Fixed seed for all six Arm A images: `424242` (re-rolls are `424243`, also logged).
- Model: **Flux3 Image Klein, no Flux2** — unet `flux3-image-klein-nvfp4.safetensors` (4.92 GB, `weight_dtype: default`) at `C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors`, text encoder `qwen3vl_4b_int8_convrot.safetensors` (type `flux3`), VAE `flux2-vae.safetensors`, KSampler 15 steps / cfg 1.0 / er_sde / simple. Resolution stays whatever the pinned graph says (1344x768) — never changed.
- ComfyUI endpoint: `http://10.13.37.88:8188` (this host). LAN-only, no auth, no API keys — never add one.
- Roster: exactly the six PDFs in `character-bible/Sheets/` (`Chip, Gulgrim, Keechwah, Rocketcandy, Shade, Vadania`). Biggins excluded — a test asserts exactly six outputs.
- All sheet/species text is copied **verbatim**; absent fields render as the exact string `(no sheet text)`; drop-list values (scores, modifiers, saves, skills, HP/AC/speed, numbers-with-`+`, feature/spell rules, currency) never appear in prompts.
- `prompts.json` entry keys, exactly: `character, arm, prompt, frame, species_sources, seed, model_hashes, workflow, output, timestamp` (`arm` is `"A"`; `output` starts `null`).
- Generated PNGs, JSON data, and workflows ARE committed (repo convention: session PNGs are tracked). No `.gitignore` changes.

## Review Focus

1. **PDF text layer is only form labels** — real values live in widget `/V` annotations; a naive `extract_text()` run silently yields empty characters. Pinned by `test_extract_sheets.py::test_real_values_not_labels` (asserts `Shade`'s name/race/class values present, and that no entry is label-only).
2. **Verbatim rule / invention leakage** — prompts must carry source text unchanged and must never borrow local-bible wording. Pinned by `test_build_sheet_bible.py::test_species_verbatim_anchors` (exact substrings from `data/species.json` appear in the prompt) and `test_build_sheet_bible.py::test_no_local_reference_reads` (script sources contain none of the forbidden tokens `bible.md`, `refs/`, `gallery`).
3. **Mechanics leakage into prompts** — drop-list terms (`Stealth`, `Saving`, `Armor Class`, `Hit Points`, `+6`-style numbers) reaching Flux as noise. Pinned by `test_build_sheet_bible.py::test_no_mechanics_in_prompts` over all six prompts.
4. **Wrong node replaced / template left behind** — swapping the prompt node could hit the wrong node or leave the S1 text or `{{PROMPT}}` sentinel. Pinned by `test_build_sheet_workflows.py::test_prompt_swap_and_untouched_graph` (new text present, `cinematic fantasy film still` absent, `{{PROMPT}}` absent, `unet_name` unchanged, every `seed`/`noise_seed` input == `424242`).
5. **Partial live run** — 4 of 6 images generating would still "look done". Pinned by `test_record_output.py::test_requires_all_six_before_complete` (verifier refuses completion unless six PNGs exist with IHDR 1344x768 and six `output` fields are non-null) plus `run_sheettest.ps1` exiting non-zero on any per-character failure.

---

### Task 1: Pin the Flux3 base workflow

**Files:**
- Create: `scripts/prepare_flux3_base.py`
- Create: `workflows/base_flux3.json` (copied graph, prompt node set to sentinel)
- Test: `tests/test_prepare_flux3_base.py`

**Interfaces:**
- Consumes: in-repo `workflows/bibleref_a_origseed.json` — Flux3 Klein text-only graph: `UNETLoader` `flux3-image-klein-nvfp4.safetensors` / `weight_dtype: default`, `CLIPLoader` `qwen3vl_4b_int8_convrot.safetensors` type `flux3`, `VAELoader` `flux2-vae.safetensors`, `KSampler` 15 steps / cfg 1.0 / er_sde / simple, `EmptyFlux2LatentImage` 1344x768, one populated `CLIPTextEncode` (an old S1 prompt) plus an empty negative encode.
- Produces: `workflows/base_flux3.json` = that graph with the populated text node's `inputs.text` == `"{{PROMPT}}"` and everything else byte-identical (sampler, steps, resolution unchanged). Later tasks rely on the sentinel contract.

- [ ] **Step 1: Verify the source graph is the expected rig (offline)**

```powershell
Select-String -Path workflows\bibleref_a_origseed.json -Pattern 'flux3-image-klein-nvfp4|qwen3vl_4b_int8_convrot|"steps": 15|"width": 1344'
```
Expected: all four patterns present. If any is missing, stop and report — the base graph changed under us; re-pin from the spec before continuing.

- [ ] **Step 2: Write the failing test**

```python
# tests/test_prepare_flux3_base.py  (unittest, offline — parses workflows/base_flux3.json)
def test_base_graph_sentinel_and_flux3_rig():
    g = json.load(open("workflows/base_flux3.json"))
    texts = [n["inputs"]["text"] for n in g.values() if "text" in n.get("inputs", {})]
    assert texts.count("{{PROMPT}}") == 1
    assert not any(t.startswith("cinematic fantasy film still") for t in texts)
    assert any(n["inputs"].get("unet_name") == "flux3-image-klein-nvfp4.safetensors" for n in g.values())
    assert any(n["inputs"].get("clip_name") == "qwen3vl_4b_int8_convrot.safetensors" for n in g.values())
    ks = next(n for n in g.values() if n["class_type"] == "KSampler")
    assert ks["inputs"]["steps"] == 15 and ks["inputs"]["cfg"] == 1.0
    lat = next(n for n in g.values() if n["class_type"] == "EmptyFlux2LatentImage")
    assert (lat["inputs"]["width"], lat["inputs"]["height"]) == (1344, 768)
```

- [ ] **Step 3: Run test to verify it FAILS** — `python -m unittest tests.test_prepare_flux3_base -v` → FAIL (file missing).

- [ ] **Step 4: Implement `scripts/prepare_flux3_base.py`**

CLI: `python scripts/prepare_flux3_base.py --src workflows/bibleref_a_origseed.json --out workflows/base_flux3.json`
Approach: load `--src`; find nodes with a non-empty `inputs.text` — require exactly one (the positive encode; the negative node's text is `""` and stays empty), else exit 2 listing the offending node ids; set it to `{{PROMPT}}`; write pretty JSON; print the changed node id.

- [ ] **Step 5: Run test to verify it PASSES** — `python -m unittest tests.test_prepare_flux3_base -v` → PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/prepare_flux3_base.py workflows/base_flux3.json tests/test_prepare_flux3_base.py
git commit -m "sheet-test: pin Flux3 Klein base workflow from bibleref graph"
```

---

### Task 2: Extract character sheet data from the PDFs

**Files:**
- Create: `scripts/extract_sheets.py`
- Create: `character-bible/sheet-test/data/sheets.json`
- Test: `tests/test_extract_sheets.py`

**Interfaces:**
- Consumes: `character-bible/Sheets/*.pdf` widget annotations (`/T` name, `/V` value) via `pypdf`.
- Produces: `data/sheets.json` = `{slug: entry}` for slug in `chip, gulgrim, keechwah, rocketcandy, shade, vadania`. Each entry (all values verbatim strings):
  `{name, race, class_level, background, alignment, faith, physical: {gender, age, height, weight, hair, skin, eyes} (absent key → "(no sheet text)"), description fields (appearance, backstory, ideals, bonds, flaws, personality): {text, boilerplate} or null, equipment: [str], weapons: [str]}`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_extract_sheets.py (unittest)
# asserts: exactly 6 slugs, no "biggins"
# test_real_values_not_labels: entry["shade"]["name"] == "Shade",
#   entry["shade"]["race"] == "Halfling", entry["shade"]["class_level"] == "Rogue 5",
#   "Rapier" in entry["shade"]["equipment"], entry["shade"]["background"] == "Criminal"
# test_physical_block_sparsity: entry["chip"]["physical"]["gender"] == "Male",
#   entry["keechwah"]["physical"] == {k: "(no sheet text)" for all 7 keys}
# test_boilerplate_flags: entry["vadania"]["appearance"]["boilerplate"] is True,
#   entry["keechwah"]["backstory"]["boilerplate"] is True,
#   entry["shade"]["backstory"]["boilerplate"] is False
# test_drop_list: no entry contains keys "str", "dex", "hp", "ac", "skills"
```

- [ ] **Step 2: Run test to verify it FAILS** — `python -m unittest tests.test_extract_sheets -v` → FAIL.

- [ ] **Step 3: Implement `scripts/extract_sheets.py`**

CLI: `python scripts/extract_sheets.py --src character-bible/Sheets --out character-bible/sheet-test/data/sheets.json`
Approach: for each PDF, iterate `page["/Annots"]` (deref `.get_object()`), collect `str(/T) = str(/V)` per widget with non-empty `/V`. Field-name map (exact): `CharacterName→name`, `RACE→race`, `CLASS  LEVEL→class_level`, `BACKGROUND→background`, `ALIGNMENT→alignment`, `FAITH→faith`, `GENDER/AGE/HEIGHT/WEIGHT/HAIR/SKIN/EYES→physical.*`, `Appearance→appearance`, `Backstory→backstory`, `Ideals→ideals`, `Bonds→bonds`, `Flaws→flaws`, `Personality→personality`, `Eq Name\d*→equipment[]`, `Wpn Name ?\d*→weapons[]` (skip proficiencies like `Wpn Prof` — only named carried items). Boilerplate rule: `is_boilerplate(text)` is True when a normalized 40-char window of `text` occurs in any `data/species.json` body (Task 3 output, loaded if present) OR in the marker file `scripts/stock_markers.txt`, seeded with two verified stock lines: `The material culture and physical characteristics of humans` (Chip's Appearance) and `You spent years learning the lore of the multiverse` (Keechwah's/Chip's stock backstory). Every description field becomes `{"text": ..., "boilerplate": bool}` or `null` when absent. Slugs = lowercased filename stems; exactly these six or exit 2.

- [ ] **Step 4: Run test to verify it PASSES** — `python -m unittest tests.test_extract_sheets -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/extract_sheets.py scripts/stock_markers.txt character-bible/sheet-test/data/sheets.json tests/test_extract_sheets.py
git commit -m "sheet-test: extract character data from DDB sheet PDF form fields"
```

---

### Task 3: Fetch and extract official DDB species details

**Files:**
- Create: `scripts/extract_species.py`
- Create: `character-bible/sheet-test/data/sources/*.html` (cached pages)
- Create: `character-bible/sheet-test/data/species.json`
- Test: `tests/test_extract_species.py`

**Interfaces:**
- Consumes: DDB legacy species pages (public, no auth): `7-tiefling, 13-dwarf, 3-elf, 14-halfling, 1-human` at `https://www.dndbeyond.com/species/<id>-<slug>`.
- Produces: `data/species.json` = `{page_slug: {url, physical: str, age_size: str, sections: {heading: str}}}` — `physical` is the concatenated verbatim paragraphs (see rule), `age_size` the verbatim `Age` and `Size` trait paragraphs, `sections` keyed by article headings (so `Hill Dwarf` / `Wood Elf` subrace sections are addressable by name).

- [ ] **Step 1: Fetch the five pages to cache (live verification)**

Script fetch step runs first so tests are offline: `python scripts/extract_species.py --fetch` (urllib with browser User-Agent, writes `data/sources/<page_slug>.html`; exits 3 if any fetch returns non-200 or <50 KB).
Expected: five cached files; spot-check `data/sources/7-tiefling.html` contains `Infernal Bloodline`.

- [ ] **Step 2: Write the failing test**

```python
# tests/test_extract_species.py (unittest, offline — parses cached HTML via species.json builder)
# test_tiefling_physical: species.json["7-tiefling"]["physical"] contains
#   "thick tails" and "horns" and "no visible sclera" (verbatim anchors)
# test_excludes_noise: physical/age_size/sections contain none of
#   "Rollback Post", "Posted May", "Male Infernal Names"
# test_subrace_sections_addressable: sections has a key containing "Hill Dwarf"
#   (13-dwarf) and one containing "Wood Elf" (3-elf)
```

- [ ] **Step 3: Run test to verify it FAILS** — `python -m unittest tests.test_extract_species -v` → FAIL.

- [ ] **Step 4: Implement the parse half of `scripts/extract_species.py`**

CLI: `python scripts/extract_species.py --sources character-bible/sheet-test/data/sources --out character-bible/sheet-test/data/species.json`
Approach (BeautifulSoup on cached HTML): locate the article body (the element containing the `# Tiefling`-style `<h1>`; comments section excluded — everything after the `Comments` heading is dropped). Physical-paragraph rule: include a `<p>` verbatim if it sits under a heading matching `(?i)description|appearance|bloodline|physique` OR under headings `Age`/`Size` (those go to `age_size` instead) OR the paragraph contains ≥2 appearance keywords from: `horn, horns, skin, hair, eyes, teeth, tusks, beard, ears, tail, fur, feathers, claws, height, build, snout, scales, tusks, lips, nose`. Skip paragraphs with `Rollback|Posted \w+ \d|Names:` markers. Headings → `sections` map (heading text → its paragraphs' verbatim concatenation).

- [ ] **Step 5: Run test to verify it PASSES** — `python -m unittest tests.test_extract_species -v` → PASS.

- [ ] **Step 6: Re-run Task 2 so boilerplate detection can use species bodies, then commit**

```bash
python scripts/extract_sheets.py --src character-bible/Sheets --out character-bible/sheet-test/data/sheets.json
python -m unittest tests.test_extract_sheets -v   # must still PASS
git add scripts/extract_species.py character-bible/sheet-test/data/sources character-bible/sheet-test/data/species.json character-bible/sheet-test/data/sheets.json
git commit -m "sheet-test: fetch and extract official DDB species details"
```

---

### Task 4: Build the sheet bible and Arm A prompts

**Files:**
- Create: `scripts/build_sheet_bible.py`
- Create: `character-bible/sheet-test/sheet-bible.md`
- Create: `character-bible/sheet-test/prompts.json` (six entries, `output: null`)
- Test: `tests/test_build_sheet_bible.py`

**Interfaces:**
- Consumes: `data/sheets.json`, `data/species.json` (Task 2/3 contracts), frame string and seed from Global Constraints.
- Produces: prompt strings and `prompts.json` per the spec's exact key list; `sheet-bible.md` mirrors each prompt under `## <name> (<slug>)` with `Sources:` lines (PDF filename + species URL).

Prompt assembly order (spec): `frame` + " " + species `physical` (+ matching `sections[<subrace>]` paragraph when `race` contains a subrace name from the map `Hill Dwarf→13-dwarf/Hill Dwarf, Wood Elf→3-elf/Wood Elf`, else base page) + " " + sheet block: `race` `, ` `class_level` `, ` `background` `, filled physical values (`gender, age, height, weight, hair, skin, eyes` — each `(no sheet text)` skipped), `equipment` joined `, `, `weapons` joined `, `, then appearance/backstory/ideals/bonds/flaws/personality texts (each suffixed ` (boilerplate)` when flagged).

Species URL map (exact): `Halfling→14-halfling, Hill Dwarf→13-dwarf, Tiefling→7-tiefling, Wood Elf→3-elf, Human→1-human`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_build_sheet_bible.py (unittest)
# test_frame_first: every prompt starts with the exact frame string; occurs exactly once
# test_species_verbatim: each prompt contains its species' verbatim anchor from species.json
#   (keechwah → "thick tails"; shade → species anchor from 14-halfling physical)
# test_sheet_verbatim: "Rapier" in shade prompt; "Plate, +2" in rocketcandy prompt
# test_no_mechanics_in_prompts: for all 6, no match of r"\b(Stealth|Saving Throw|Armor Class|Hit Points|Proficiency|\+\d+)\b"
# test_no_local_reference_reads: for every scripts/*.py, source contains none of
#   ["bible.md", "refs/", "gallery"]
# test_prompts_json_schema: 6 entries; keys == exactly the 9 spec keys;
#   arm == "A"; seed == 424242; frame == frame string; output is None;
#   species_sources values match the URL map; model_hashes.unet_name == flux3-image-klein-nvfp4.safetensors
# test_sheet_bible_mirrors: every prompts.json prompt appears in sheet-bible.md
```

- [ ] **Step 2: Run test to verify it FAILS** — `python -m unittest tests.test_build_sheet_bible -v` → FAIL.

- [ ] **Step 3: Implement `scripts/build_sheet_bible.py`**

CLI: `python scripts/build_sheet_bible.py --data character-bible/sheet-test/data --out-dir character-bible/sheet-test --model-path "C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors"`
Approach: assemble prompts per Interfaces; `model_hashes` = `{"unet_name": "flux3-image-klein-nvfp4.safetensors", "sha256": <streamed hashlib of model file>}` (one-time, 4.92 GB — seconds); `workflow`: `"workflows/base_flux3.json"`; `timestamp`: ISO-8601 now; write `prompts.json` + `sheet-bible.md`.

- [ ] **Step 4: Run test to verify it PASSES** — `python -m unittest tests.test_build_sheet_bible -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_sheet_bible.py character-bible/sheet-test/sheet-bible.md character-bible/sheet-test/prompts.json tests/test_build_sheet_bible.py
git commit -m "sheet-test: build Arm A prompts from sheet + species sources"
```

---

### Task 5: Generate the six workflow JSONs

**Files:**
- Create: `scripts/build_sheet_workflows.py`
- Create: `workflows/sheettest_<slug>.json` ×6
- Test: `tests/test_build_sheet_workflows.py`

**Interfaces:**
- Consumes: `prompts.json` (Task 4), `workflows/base_flux3.json` sentinel contract (Task 1).
- Produces: six API-format graphs identical to base except: `{{PROMPT}}` node text = that character's prompt; every `seed`/`noise_seed` input = `424242`; the `SaveImage` node's `filename_prefix` = `sheettest_<slug>`; filenames `workflows/sheettest_{chip,gulgrim,keechwah,rocketcandy,shade,vadania}.json`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_build_sheet_workflows.py (unittest)
# test_prompt_swap_and_untouched_graph (Review Focus #4): for each of 6 files:
#   its prompt text from prompts.json present; "{{PROMPT}}" absent;
#   "cinematic fantasy film still" absent; unet_name still flux3-image-klein-nvfp4.safetensors;
#   SaveImage filename_prefix == "sheettest_<slug>";
#   every inputs key in {"seed","noise_seed"} == 424242; file size within 20% of base (graph structure unchanged)
# test_exactly_six: set of workflows/sheettest_*.json == the six slugs
```

- [ ] **Step 2: Run test to verify it FAILS** — `python -m unittest tests.test_build_sheet_workflows -v` → FAIL.

- [ ] **Step 3: Implement `scripts/build_sheet_workflows.py`**

CLI: `python scripts/build_sheet_workflows.py --base workflows/base_flux3.json --prompts character-bible/sheet-test/prompts.json --out-dir workflows`
Approach: deep-copy base per entry; find node with `inputs.text == "{{PROMPT}}"` (exactly one, else exit 2); set to entry prompt; walk all nodes setting `inputs["seed"]`/`inputs["noise_seed"]` = `424242` when the key exists; set the single `SaveImage` node's `inputs.filename_prefix` to `sheettest_<character>` (exactly one, else exit 2); write `sheettest_<character>.json`.

- [ ] **Step 4: Run test to verify it PASSES** — `python -m unittest tests.test_build_sheet_workflows -v` → PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_sheet_workflows.py workflows/sheettest_*.json tests/test_build_sheet_workflows.py
git commit -m "sheet-test: generate per-character workflow JSONs with fixed seed"
```

---

### Task 6: Run the six generations and record outputs

**Files:**
- Create: `scripts/run_sheettest.ps1`
- Create: `scripts/record_output.py` + `character-bible/sheet-test/img/<slug>.png` ×6
- Create: `scripts/verify_sheettest.py` (completion gate)
- Modify: `character-bible/sheet-test/prompts.json` (`output` + final `timestamp` filled)
- Test: `tests/test_record_output.py`

**Interfaces:**
- Consumes: `workflows/sheettest_*.json`, ComfyUI HTTP API (`POST /prompt`, `GET /history/<id>`, `GET /view?filename=&subfolder=&type=output`), `prompts.json`.
- Produces: completed `prompts.json` (`output: "img/<slug>.png"`) and six PNGs at `img/<slug>.png`, 1344x768.

- [ ] **Step 1: Write the failing test (pure parts only)**

```python
# tests/test_record_output.py (unittest, fixtures — no server)
# test_record_output_updates_entry: record_output(recorded, "shade", "img/shade.png", ts)
#   → entry["shade"]["output"] == "img/shade.png", timestamp == ts, other entries untouched
# test_requires_all_six_before_complete: verify_sheettest.complete(prompts, img_dir) is False
#   with 5 PNGs / one null output; True with 6 PNGs whose IHDR bytes (offset 16..24,
#   big-endian) == (1344, 768) and six non-null outputs
# test_png_header_parse: parse_ihdr on a minimal crafted PNG header returns (1344, 768)
```

- [ ] **Step 2: Run test to verify it FAILS** — `python -m unittest tests.test_record_output -v` → FAIL.

- [ ] **Step 3: Implement `scripts/record_output.py` and `scripts/verify_sheettest.py`**

`python scripts/record_output.py --prompts character-bible/sheet-test/prompts.json --character <slug> --output img/<slug>.png --timestamp <iso>` (in-place JSON update).
`python scripts/verify_sheettest.py --prompts ... --img character-bible/sheet-test/img` → prints `COMPLETE` + table, exit 0; else lists missing/mismatched, exit 1 (Review Focus #5).

- [ ] **Step 4: Run test to verify it PASSES** — `python -m unittest tests.test_record_output -v` → PASS.

- [ ] **Step 5: Run the live generation (manual-paced, observable)**

```powershell
.\scripts\run_sheettest.ps1 -Host 10.13.37.88 -Port 8188
```
`run_sheettest.ps1` behavior: GET `/system_stats`, print VRAM free (warn only if < 4 GB); for each of the six slugs: read workflow JSON → `POST /prompt` with `{"prompt": <graph>, "client_id": "sheet-test-<slug>"}` → poll `GET /history/<prompt_id>` until the entry appears (30 s timeout, 5 s interval) → `GET /view?filename=<output file>&subfolder=&type=output` → write `img/<slug>.png` → call `record_output.py` → next; any failure: print `FAILED <slug>: <reason>` and exit 1 immediately (no silent partials).

- [ ] **Step 6: Verify completion**

```powershell
python scripts/verify_sheettest.py --prompts character-bible/sheet-test/prompts.json --img character-bible/sheet-test/img
```
Expected: `COMPLETE`, exit 0. Then `python -m unittest discover -s tests -v` → all suites PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/run_sheettest.ps1 scripts/record_output.py scripts/verify_sheettest.py character-bible/sheet-test/img character-bible/sheet-test/prompts.json tests/test_record_output.py
git commit -m "sheet-test: run six Arm A generations and record outputs"
```

---

## Handoff to the human

After Task 6: report the six image paths and remind the human that side-by-side judgment against `character-bible/refs/` happens in `character-bible/sheet-test/NOTES.md`, which the human creates at comparison time (spec: comparison verdicts are the human's; the agent does not write them).
