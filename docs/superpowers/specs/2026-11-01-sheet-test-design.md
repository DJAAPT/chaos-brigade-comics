# Sheet-Test — character sheets as the basis for bible reference images

Date: 2026-11-01
Status: approved 2026-11-01; amended 2026-11-01 per user — **Flux3 replaces
Flux2 as the generation engine (no Flux2 in this test)**. Rationale: the test
ignores everything done before — fresh engine alongside fresh prompt basis,
so nothing carried over can influence the result.
Scope: experiment (Arm A first, Arm B kept possible)

## Intent

Test empirically whether D&D Beyond character sheets — plus official DDB
species ("race") details — **alone** can serve as the basis for bible
reference images, as an alternative to the gallery-grounded method that
produced `character-bible/bible.md` v2. This is a **comparison**, not a
replacement: the locked bible, the approved reference images, and the local
gallery play no part in this test's generation path and are not modified.

Success looks like: six new solo reference images, one per character, each
traceable to a prompt built only from that character's sheet text and their
species' official DDB text, ready to be judged side-by-side against the
approved gallery-grounded refs. A useful negative result (this basis is too
thin to carry a look) counts as success — it is the question being asked.

## Goals

- Arm A (this pass): prompts built **only** from (a) sheet text, literal
  structured extract, and (b) official DDB species detail text for the
  character's race (user decision: race details are part of the baseline).
- One solo portrait per character into a new directory
  `character-bible/sheet-test/` — parallel to, never inside, the approved set.
- Full audit trail: prompt, seed, model hashes, and source URLs logged per
  image.
- Layout designed so Arm B (interpreted translation) can be added later as a
  second arm without rework.
- Side-by-side comparison against the existing approved refs, verdicts
  recorded in a notes file, judged by the human. (Existing Flux3 runs in
  `sessions/flux3-test/` used the same Flux3 graph with old prompts, so a
  prompt-only axis against same-engine reruns also exists; which baselines
  count remains the human's call in `NOTES.md`.)

## Non-goals / anti-goals

- Not replacing or editing `character-bible/bible.md` (LOCKED) or any
  approved image. Nothing in `character-bible/refs/` or the gallery at
  `O:\ExternalSites\html\DND\gallery\` is read during prompt construction.
- No local gallery images, no old locked-chunk wording, no approved
  portraits in the generation path. If an Arm A prompt contains a phrase
  that also exists in the old bible, it must be because the sheet or the
  official species text says it too.
- Official DDB species **art** is not wired into generation in Arm A
  (species art = text inspiration only for now; using it as image
  conditioning would be a separate later arm).
- No image-based identity tools (IP-Adapter / ReActor / face matching) —
  text-only, so the test measures what this text basis can carry.
- Not building the v2 automation (`scripts/new-session.ps1`) — manual runs,
  same style as the S1 v1 flow.
- No comparison verdict written by the agent — side-by-side judgment is the
  human's.

## Constraints

- **Inputs (access settled — no browser sign-in needed):** character sheets
  live at `character-bible/Sheets/{Chip,Gulgrim,Keechwah,Rocketcandy,Shade,Vadania}.pdf`.
  These are DDB printable-sheet PDFs whose visible text layer is only form
  labels; real values live in widget annotations (`/V`). Extraction uses
  `pypdf` (installed, verified: e.g. Shade = `CharacterName = Shade`,
  `RACE = Halfling`, `CLASS  LEVEL = Rogue 5`, `Eq Name0 = ...`).
- **Roster settled:** the six PDFs are the deliverable set. All six have
  approved baseline refs in `character-bible/refs/` (builder-verified), so
  there are no "no baseline" cases.
- **Race details source:** official DDB legacy (2014) species pages,
  publicly readable: tiefling `/species/7-tiefling`, dwarf `/species/13-dwarf`
  (Hill Dwarf section), elf `/species/3-elf` (Wood Elf section),
  halfling `/species/14-halfling`, human `/species/1-human`. Verified: pages
  server-render article text including rich physical descriptions (e.g.
  tiefling horns/tail/eyes/skin/hair) plus Age/Size traits.
- **Generation rig (amended 2026-11-01 per user): Flux3, no Flux2 at all.**
  ComfyUI at `10.13.37.88:8188` (this host, verified), **Flux3 Image Klein**:
  unet `flux3-image-klein-nvfp4.safetensors` (4.92 GB step-distilled,
  `C:\DEV\ComfyUI\models\diffusion_models\`), text encoder
  `qwen3vl_4b_int8_convrot.safetensors` (CLIPLoader type `flux3`), VAE
  `flux2-vae.safetensors` (Flux3 reuses it), 1344x768, KSampler 15 steps /
  cfg 1.0 / er_sde / simple. All model files verified on disk; rig documented
  in `FLUX3-SETUP.md`. The prompt upsampler and the undistilled base model
  are not installed and not used — bible-style prompts go in verbatim.
- **Base workflow:** `workflows/bibleref_a_origseed.json` — an in-repo Flux3
  Klein text-only graph with exactly one populated `CLIPTextEncode` node
  (carrying an old S1 prompt) — is copied to `workflows/base_flux3.json`
  with that node set to sentinel `{{PROMPT}}`; sampler, steps and resolution
  stay byte-identical. Backup: ComfyUI `/history` still contains
  Flux3-Klein runs (verified) should the file be lost.
- Never commit API keys. Remote is LAN-only, no auth (README conventions).
- Biggins excluded (already LOCKED from `gallery/NPCs/Biggans_Aulswim.png`;
  no sheet provided).

## Approaches considered

1. **Structured literal extract (Arm A — chosen).** Copy imageable sheet
   fields in the player's own words; add official species physical-detail
   text; drop purely mechanical blocks. Purest test: weak results mean
   "this basis lacks visual specificity", not "the agent glossed it".
2. **Visual translation (Arm B — deferred, kept possible).** Agent reads a
   sheet and writes the prompt in its own words under extraction rules the
   human approved once. Directory/log layout reserves room for it.
3. **Verbatim everything including stat blocks (rejected).** "14 AC,
   Stealth +8" is noise to a diffusion model; it would fail the test for
   trivial reasons and teach nothing.

## Arm A — how it works

### 1. Sheet extraction (per character)
From each PDF's widget fields, capture verbatim:

**Take:**
- `CharacterName`, `RACE` (+ subrace field when one exists), `CLASS  LEVEL`,
  `BACKGROUND`, `ALIGNMENT`, `FAITH`
- physical block when filled: `GENDER`, `AGE`, `HEIGHT`, `WEIGHT`, `HAIR`,
  `SKIN`, `EYES`
- appearance/description fields (`Appearance`, `Backstory`, `Ideals`,
  `Bonds`, `Flaws`, `Personality`) — verbatim, flagged `(boilerplate)` when
  the text is clearly stock DDB species/background prose rather than written
  about the character (known cases: Vadania's Appearance = wood-elf species
  text, Chip's Appearance = generic human-culture line; Keechwah/Chip
  backstories are stock background text)
- worn/visible equipment from `Eq Name*` and `Wpn Name*` fields (e.g.
  Rocketcandy `Plate, +2`, `Shield`, `Holy Symbol`; Vadania
  `Monster Hunter's Longbow, +1`, `Leather`; Shade `Leather`, `Rapier`,
  `Dagger`)

**Drop:** ability scores, modifiers, saves, skills, HP/AC/speed, proficiency
numbers, feature/spell rules prose, spell lists, currency/weight numbers.

**Hard rules:** player-written words are copied, never reworded; never
import wording from `bible.md` or the gallery set; absent field →
`(no sheet text)`, never filled in.

Recon finding recorded: the physical block is filled ONLY on Chip's sheet
(Male, 35, 5'11", 172, White skin, Brown eyes, Brown hair); the other five
left it blank. Shade's backstory is richly personal; that is the exception.

### 2. Species detail extraction (per race, once per species)
From the official DDB species page (URLs under Constraints), capture
**verbatim**:
- the physical-appearance sentences of the article body (for tiefling: the
  "Infernal Bloodline" paragraph — horns variety, thick 4–5 ft tail,
  pointed canines, solid-color eyes with no sclera or pupil, skin incl.
  shades of red, dark hair)
- the `Age` and `Size` trait sentences
- the subrace section's own physical/trait sentences when the sheet names a
  subrace (Hill Dwarf, Wood Elf, etc.)

**Drop:** name lists, history/culture/lore sections, gameplay traits
(darkvision, resistances, damage), quoted fiction blurbs, and the page's
forum comments.

Source URL logged per species. Article body only — no comment threads.

Note recorded (not resolved here): official species text may conflict with
the locked bible's looks (e.g. canon tiefling tails vs the old set). Test
images are not replacing the bible; divergences are comparison findings, to
be written down, not corrected in this pass.

### 3. Prompt assembly
`solo full-body portrait of a single character, plain background` + `[species
physical details verbatim]` + `[sheet: race/subrace, class & level,
background, physical block, visible equipment, personal description fields]`

- The frame is composition only — no style words, no character content —
  identical for every character, so it cancels out of the comparison.
- **No global anti-drift suffix.** Derived from failures with the old image
  set; only fights drift *between* panels, which a single portrait has none
  of.

### 4. Generation
- One workflow JSON per character from `workflows/base_flux3.json` (pinned
  from `bibleref_a_origseed.json`) + assembled prompt.
- Submit to `10.13.37.88:8188`, poll history, download to
  `character-bible/sheet-test/img/<character-slug>.png`.
- One fixed seed for all Arm A images (comparability; re-roll = seed+1,
  also logged).

### 5. Logging
`character-bible/sheet-test/prompts.json` — array of entries:
`{ character, arm: "A", prompt, frame, species_sources, seed, model_hashes, workflow, output, timestamp }`

### 6. Comparison (later, human)
`character-bible/sheet-test/NOTES.md` — side-by-side of each sheet-test image
vs the approved ref for that character, verdict and observations recorded by
the human. What Arm B should add (or whether this basis simply can't carry a
look) is written there.

## Directory layout

```
character-bible/
  Sheets/               # input: exported DDB sheet PDFs (human-provided)
  bible.md              # LOCKED, untouched
  refs/                 # approved refs, untouched
  sheet-test/
    sheet-bible.md      # Arm A prompt blocks, verbatim extracted text + sources
    prompts.json        # audit log
    img/                # generated reference PNGs
    NOTES.md            # human comparison verdicts (created at comparison time)
    (later) arm_b/      # Arm B prompts + images, same log format
```

## Builder-check answers (recorded)

1. Base workflow → superseded by the Flux3 amendment: pinned from in-repo
   `workflows/bibleref_a_origseed.json` into `workflows/base_flux3.json`
   (ComfyUI `/history` still holds Flux3-Klein runs as backup).
2. Weight file → answered for the original Flux2 plan
   (`flux2_dev_fp8mixed.safetensors`, S1 run log + README); superseded by the
   2026-11-01 Flux3 amendment — now `flux3-image-klein-nvfp4.safetensors`.
3. Roster scope → the six provided sheets; all six have baselines; the
   no-baseline case does not occur.

## Open items

None blocking. Tooling note: `pypdf` was installed (user site) for PDF
extraction; it is read-only tooling, not a project dependency.

## Arm B — Round 2 directive (approved-in-concept 2026-11-02, awaiting doc approval)

Human verdict on round 1: six images are decent starting points and stay
**frozen** as the clean-sheet baseline (they are the comparison arm).
Two named defects: Rocketcandy's prompt pulled his sheet-listed Shield and
his arm reads missing; Shade renders as a toddler instead of a small adult.

Round 2 = **Approach 1: merged text only.** One authored combined
description per character merging, for each character: sheet facts,
official DDB species canon (same URLs), the locked-chunk wins from the
current `character-bible/bible.md` (main checkout — e.g. `grown man in
his 30s, NOT child`, `exactly two arms`, `NO wings`), and the new
reference-sheet composition rules. Single changed variable vs round 1:
the prompt. Same Flux3 graph, same seed 424242, same frame prefix.

**New reference-sheet composition rules (human, 2026-11-02):**
- Nothing occludes the figure: no shields, no gear held across the body.
  Stowed gear (at hips, on back) stays.
- Both arms clearly visible; exactly two arms per humanoid.
- Small races get explicit adult proportions (`small adult man ... NOT a
  child`).

**Round-2 constants:**
- Frame stays byte-identical to round 1
  (`solo full-body portrait of a single character, plain background`)
  and is followed by a second constant addendum:
  `standing neutral pose, both arms clearly visible, no shield, nothing held across the body`.
- Prompt = frame + addendum + authored combined description.

**Structure (script stays bible-free by design):** the agent authors
`character-bible/sheet-test/arm_b/descriptions.md` — six blocks with
per-block source lines (sheet PDF + species URL + "bible.md locked
chunks") — after reading all three inputs directly. A build script then
assembles `arm_b/prompts.json` (same nine-key schema, `arm: "B"`) and
`workflows/sheettest_b_<slug>.json` (`SaveImage` prefix
`sheettest_b_<slug>` so ComfyUI outputs never collide with round 1)
purely from `descriptions.md` + constants. No script ever reads
`bible.md`, so the Round-1 forbidden-token guard stays untouched.

**Example block (Rocketcandy — the flagged character):**
> adult male human paladin in his early 30s, short brown hair, light
> stubble, stern noble bearing, shining full plate armor with a gold
> phoenix crest on the chest, long red cape flowing behind him, gold
> signet ring, holy symbol of Bahamut at his belt, battleaxe at his hip,
> exactly two arms

**Layout:** `character-bible/sheet-test/arm_b/{descriptions.md,
prompts.json, img/<slug>.png}`; runner gets `-PromptsPath`/`-ImgDir`
parameters (defaults keep round-1 behavior byte-identical). Round-1
files are never rewritten by round 2.

**Comparison:** human side-by-side of `img/` vs `arm_b/img/` in
`NOTES.md` (human's file, per spec).

## Arm C — Round 3 directive (framing experiment, awaiting doc approval)

Human verdict on Arm B: direction approved — keep `arm_b/` frozen as the
second comparison point. New requirement: bible reference images must be
**head-to-toe full body** with a **consistent camera distance across all
six** so size differences (Shade ~3 ft vs humans ~5–6 ft) are readable.

**Round 3 = framing only.** Prompt = new frame + the byte-identical
Arm B addendum + the byte-identical Arm B block (blocks read from
`arm_b/descriptions.md` itself — nothing re-authored). Single changed
variable vs Arm B: the frame clause.

**New frame (verbatim, the ONLY change):**
`solo full-body portrait of a single character, head-to-toe full body with feet visible and empty space above the head, stationary camera at a fixed distance, plain background`

(Invariant: removing the inserted clause from the Arm C frame yields the
Arm B frame byte-for-byte — the clause is the experiment.)

**Reserved follow-up (not built now):** if wording-only framing proves
too weak on size cues, Arm C-2 adds a constant scale object beside every
character (ordinary wooden door ≈ 6.5 ft ruler, beside never across the
figure) — human decides after seeing round-3 results.

**Round-3 constants:** same Flux3 graph, seed 424242, same addendum, same
blocks, roster of six. Layout: `character-bible/sheet-test/arm_c/`
(`prompts.json` with `arm: "C"`, `img/<slug>.png`); workflows
`workflows/sheettest_c_<slug>.json`; builder gains `--frame` (default =
Arm B frame, byte-identical round-2 behavior); runner parameters reused.
Arm A (`img/`) and Arm B (`arm_b/`) are never written by round 3.

## Shade Lab directive (single-character wording experiment, awaiting doc approval)

Human verdict on Arm C: most characters good; **Shade still wrong** —
weird face with elf ears. Canon: halflings have ordinary human features
at half size (a full-size adult with every feature scaled down
uniformly). Door ruler declined — feature sizes read clearly enough.

**Root cause recorded:** the arm blocks carry the chunk's positive
"ears small and rounded" but never the bible NEVER-list bans; "halfling"
triggers the model's pointy-ear prior. Fix = explicit guards in Shade's
block (chunk stays verbatim; additions around it, established pattern),
reusing the bible's NEVER wording:

> …belt dagger at hips, **full-size adult human features scaled down
> uniformly to half size, same proportions as a grown man, small rounded
> human ears, no pointed ears, no elf ears, no large ears, no protruding
> ears,** exactly two arms

**Batch (human-approved):** one revised block × **4 seeds** —
`424242` (control: identical to Arm C's Shade seed, so wording is the
only delta), `424243` (documented +1 re-roll), `777001`, `314159`
(independent seeds already used in this repo's workflow history).

**Layout:** `character-bible/sheet-test/shade-lab/`
(`descriptions.md` single `## Shade (shade_s0)`-style block source,
`prompts.json` with four entries keyed `shade_s0..shade_s3` carrying
their own `seed` values, `img/shade_s<N>.png`); workflows
`workflows/shadelab_shade_s<N>.json`.

**Plumbing changes (production defaults stay byte-identical):**
- `build_sheet_workflows.build_one` gains `seed=None` → defaults to the
  current constant; main passes each entry's own `seed` (arms' entries
  all say 424242, so arm outputs stay byte-identical — parity tests pin it).
- Runner's "exactly six" setup guard relaxes to "at least one" (the arms'
  completeness contract lives in `verify_sheettest`'s exact-roster gate,
  unchanged).
- `verify_sheettest` gains optional `--roster` (default = the six arm
  slugs, byte-identical default behavior); lab verifies with its four
  keys.
- Lab build via a small `scripts/build_shadelab.py` reusing
  `build_arm_b`'s frame/addendum/parser constants; production builders
  otherwise untouched.

**Success check:** all four lab images show ordinary human ears on a
scaled-down adult — especially the `424242` control versus Arm C's Shade
(same seed, wording is the only delta). Arms A/B/C stay frozen.
