# Shade Identity Fix + Ask-Don't-Guess Rule — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Shade's bible entry with the approved v4 look, harden the global ban suffix against age drift, and add an ask-don't-guess rule so unstated characters/details are questioned, never invented.

**Architecture:** Two markdown files carry the whole change: `character-bible/bible.md` (the locked prompt source) and `scene-director/director.md` (where prompts get assembled). No code, no tests in the TDD sense — verification is grep-based consistency checks against the exact strings in this plan.

**Tech Stack:** Markdown (GitHub-flavored), PowerShell/grep for verification.

**Spec:** Approved design from the 2026-11-01 brainstorming session (recorded in this session's conversation): Shade = young adult halfling man, mid-20s, lean, dark brown shaggy hair, light stubble, guarded watchful expression, human ears, worn linen shirt + brown leather vest; new global bans for gray/white hair; ask-don't-guess rule in bible + director.

## Global Constraints

- `character-bible/bible.md` is LOCKED — update only with approval. This plan IS the approval (user approved the design 2026-11-01).
- Approved identity reference: `character-bible/approved_shade_reference.png` (already saved; do not regenerate or rename).
- `character-bible/approved_S1P1_reference.png` stays as-is (accepted variance — S1P1 shows Shade in brown studded armor).
- All new prompt wording must be copy-pasteable verbatim into a Flux prompt — no placeholders, no "TBD".
- Never commit Comfy API keys (existing repo rule).

## Review Focus

- **Leftover old-Shade wording:** Any surviving "30s", "short stature", or "SHORT adult man" text will re-summon the old-man render on the next generation. Test: grep for each of those strings after edits; expected zero hits in `bible.md`.
- **Rule not reachable at generation time:** The ask-don't-guess rule must sit where prompts are actually assembled (`director.md`), not only in the bible. Test: grep `director.md` for the rule keyword; expected one hit.
- **NEVER-list regression:** Dropping "hobbit feet" or adding it twice while rewriting the Shade entry. Test: read the final Shade block in full after edit; count occurrences of each NEVER item.
- **Global suffix drift:** The suffix line is appended to EVERY prompt — a typo there affects every panel. Test: grep for `no gray hair, no white hair` in the suffix line; expected exactly once, in the suffix, not only in Shade's entry.
- **Reference file existence:** Bible points at a file that must exist. Test: `Test-Path` on `approved_shade_reference.png`; expected True.

---

### Task 1: Update global suffix + add ask-don't-guess rule in bible.md

**Files:**
- Modify: `character-bible/bible.md:3` (rule line), `character-bible/bible.md:9` (global suffix)

**Interfaces:**
- Consumes: nothing
- Produces: the amended global suffix string (later task's Shade entry assumes the suffix already bans gray/white hair); the ask-don't-guess rule text (Task 2 references it in director.md by name, not by copy)

- [ ] **Step 1: Add the ask-don't-guess rule after line 3**

In `character-bible/bible.md`, directly after the line beginning `Rule: NEVER invent new faces`, insert:

```markdown
Rule: ASK, DON'T GUESS — if a panel needs a character, outfit, object, or scene detail with no entry in this bible, STOP and ask before generating. A generated guess becomes canon in later panels. Applies to me when directing scenes and to any automated pipeline step.
```

- [ ] **Step 2: Amend the global suffix**

Replace the current global suffix line (line 9, currently starting `adult faces, no children, no teens, exactly two arms per humanoid`):

```markdown
Global suffix (append to EVERY prompt):
`adult faces, no children, no teens, no gray hair, no white hair, exactly two arms per humanoid, single character each, no duplicates, no conflation, no extra heads, no wings unless noted, photorealistic, highly detailed`
```

The only textual delta is inserting `no gray hair, no white hair, ` after `no teens, `. Everything else in the line stays byte-identical.

- [ ] **Step 3: Verify both edits**

Run:
```powershell
Select-String -Path "character-bible\bible.md" -Pattern "ASK, DON'T GUESS" | Measure-Object | Select-Object -ExpandProperty Count
Select-String -Path "character-bible\bible.md" -Pattern "no gray hair, no white hair" | Measure-Object | Select-Object -ExpandProperty Count
```
Expected: `1` and `1`.

- [ ] **Step 4: Commit**

```bash
git add character-bible/bible.md
git commit -m "bible: add ask-don't-guess rule, ban gray/white hair globally"
```

---

### Task 2: Replace Shade's locked entry with the approved v4 look

**Files:**
- Modify: `character-bible/bible.md:13-16` (current Shade block: heading, prompt chunk, refs line, guild mark line)

**Interfaces:**
- Consumes: `character-bible/approved_shade_reference.png` (exists from the brainstorming session)
- Produces: Shade's new locked prompt chunk — any later panel-generation step copies this verbatim

- [ ] **Step 1: Replace the four-line Shade block**

Delete the current block:

```markdown
### Shade — Male Halfling Rogue (St3v3D/David). SHORT adult man, NOT child.
`adult halfling man, short stature, grown man in his 30s, light stubble, brown hair, leather rogue armor, dual daggers at hips`
Refs: gallery/Scenes/Shade_joins_the_guild.png (tattoo scene, adult face), Shade_and_Brother_Sean.png, St3v3D_Chaos_Brigade.png (front, small size). NEVER: child, boy, teen, hobbit feet.
Guild mark: geometric diamond tattoo (gallery/Objects/The_Tattoo.png) on forearm — include only when plot-relevant.
```

Replace it with:

```markdown
### Shade — Male Halfling Rogue (St3v3D/David). Young adult halfling man, NOT child, NOT elderly.
`young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair, light stubble, no beard, warm brown eyes, guarded watchful expression, human ears with rounded lobes, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, belt dagger at hips`
Approved identity ref (2026-11-01): `character-bible/approved_shade_reference.png` — copy this face for any new Shade portrait; other gallery refs show pointed ears or wrong builds, face is secondary to this one.
NEVER: child, boy, teen, elderly, gray hair, white hair, beard, wrinkles, pointed ears, elf ears, hobbit feet, bare feet, blond hair, big friendly smile by default.
Default expression: guarded, watchful, quietly assessing — keep-to-himself thief, not the outgoing one.
Guild mark: geometric diamond tattoo (gallery/Objects/The_Tattoo.png) on forearm — include only when plot-relevant.
```

- [ ] **Step 2: Verify no old-Shade wording survives**

Run:
```powershell
Select-String -Path "character-bible\bible.md" -Pattern "30s|short stature|SHORT adult man" | Measure-Object | Select-Object -ExpandProperty Count
Test-Path "character-bible\approved_shade_reference.png"
```
Expected: `0` and `True`.

- [ ] **Step 3: Read the final Shade block in full**

Confirm: heading present, prompt chunk in backticks on one line, approved ref line present, NEVER line has exactly one `hobbit feet` and one `pointed ears`, guild mark line unchanged from original.

- [ ] **Step 4: Commit**

```bash
git add character-bible/bible.md
git commit -m "bible: lock Shade to approved v4 look (young adult, dark brown hair, guarded)"
```

---

### Task 3: Add the ask-don't-guess line to director.md

**Files:**
- Modify: `scene-director/director.md:20-24` (Prompt assembly section)

**Interfaces:**
- Consumes: the rule from Task 1 (referenced by name; wording lives in bible.md — do not fork the text)
- Produces: none (terminal task)

- [ ] **Step 1: Add the rule to Prompt assembly**

In `scene-director/director.md`, under the `## Prompt assembly` heading, after the line `Always append character-bible anti-conflation footer.`, insert:

```markdown
If any character, outfit, object, or scene detail needed for a panel has no bible entry: STOP and ask the user before generating — never invent (bible: "ASK, DON'T GUESS").
```

- [ ] **Step 2: Verify**

Run:
```powershell
Select-String -Path "scene-director\director.md" -Pattern "ASK, DON'T GUESS" | Measure-Object | Select-Object -ExpandProperty Count
```
Expected: `1`.

- [ ] **Step 3: Commit**

```bash
git add scene-director/director.md
git commit -m "director: enforce ask-don't-guess before prompt assembly"
```

---

### Task 4: Final consistency sweep

**Files:**
- Read-only check across `character-bible/bible.md` and `scene-director/director.md`

**Interfaces:**
- Consumes: Tasks 1-3
- Produces: none (verification only)

- [ ] **Step 1: Run the full sweep**

```powershell
$p = Select-String -Path "character-bible\bible.md" -Pattern "ASK, DON'T GUESS" | Measure-Object | Select-Object -ExpandProperty Count
$s = Select-String -Path "character-bible\bible.md" -Pattern "no gray hair, no white hair" | Measure-Object | Select-Object -ExpandProperty Count
$o = Select-String -Path "character-bible\bible.md" -Pattern "30s|short stature|SHORT adult man" | Measure-Object | Select-Object -ExpandProperty Count
$d = Select-String -Path "scene-director\director.md" -Pattern "ASK, DON'T GUESS" | Measure-Object | Select-Object -ExpandProperty Count
$r = Test-Path "character-bible\approved_shade_reference.png"
"rule=$p suffix=$s oldShade=$o director=$d refExists=$r"
```
Expected: `rule=1 suffix=1 oldShade=0 director=1 refExists=True`.

- [ ] **Step 2: Visual check of bible.md top section**

Read `character-bible/bible.md` lines 1-20. Confirm rule order reads: title → approved refs → never-invent rule → ask-don't-guess rule → why-drift section → global suffix → Shade block.

- [ ] **Step 3: Final commit if anything was touched**

```bash
git status
# if dirty:
git add -A
git commit -m "chore: shade identity fix consistency sweep"
```
