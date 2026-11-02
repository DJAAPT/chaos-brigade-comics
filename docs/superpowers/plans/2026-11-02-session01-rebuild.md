# Session 1 Comic Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the session 1 comic end-to-end under the new bible, Flux3 pipeline, and standing readability rules — ~21 new panel generations plus assembly of the full HTML comic.

**Architecture:** One task per script page-batch (generate → user reviews renders → approve → next), then a final assembly task (HTML + panels.json). Prologue and dramatis personae need no generations (approved portraits + lineup already exist). Every generation derives from `workflows/base_flux3.json` with locked bible chunks; prompts, seeds, and outputs logged per the director's assembly rule.

**Tech Stack:** Flux3 Klein via ComfyUI MCP tools, PowerShell file ops, HTML comic assembly.

**Spec:** `sessions/session01/script.md` (5 pages, 20 panels, approved beats/quotes) + `scene-director/director.md` readability rules (2026-11-02) + design decisions in this session's conversation.

## Global Constraints

- Commits to `main` (standing consent, this repo/session).
- Every panel prompt uses current locked bible chunks verbatim + global suffix; Flux3 only; `workflows/base_flux3.json` as the graph source (new workflow JSON per panel, kept in `workflows/`).
- Quote discipline (director rule): speech traceable to transcript lines; narration in DM voice.
- NPCs without approved portraits (Marigold, Sammy, proprietor, butler, Filvenar, guards) generate from bible text only; reuse the same seed per recurring NPC within the session for consistency.
- STOP-and-ask triggers from the bible/director stay live: any needed detail with no entry gets asked, never invented (record the question, don't guess).
- User approves each batch's renders before the next batch generates (\RULE unanimous in this session: generate → present → verdict → proceed).

## Review Focus

1. **Unapproved-NPC drift** — Marigold appears in 4+ panels with no portrait lock; same face must recur. Pin: reuse one fixed seed for her across all panels; reviewer checks her face across P1.1/P1.2/P2.1/P2.4/P3.3.
2. **Water Bear owlbear risk** — one owl-head + bear body + no wings is a known-hard composition. Pin: Task 5 generates P4.1 first and stops for verdict before the rest of page 4.
3. **Dropped-character recurrence** — P1.1 v1 merged Gulgrim/Chip; any 5+ figure panel can drop or merge. Pin: every batch's test counts distinct figures against the script before presenting.
4. **Quote traceability** — assembly must not invent dialogue. Pin: Task 7 checks every speech line against transcript/script before writing HTML.
5. **panels.json completeness** — every shipped panel needs its log entry (prompt, seed, model, file). Pin: Task 7 asserts one entry per image file.

---

### Task 1: Docks seed panel (new — readability rule)

**Files:**
- Create: `workflows/flux3_s1_docks.json`
- Output: `sessions/session01/panel0_docks.png`

**Interfaces:**
- Consumes: `workflows/base_flux3.json`
- Produces: approved docks panel establishing the tattoo plot language.

- [ ] **Step 1: Generate** — Rocketcandy (crest, axe) clasping forearms with a corrupt guard (red plume, red cape, diamond wrist tattoo close-up visible), Shade watching from the side, Neverwinter docks background, warm daylight. Locked chunks for Rocketcandy + Shade; guard per bible corrupt-guard block.
- [ ] **Step 2: Present render, get user verdict** (iterate on feedback, same loop as portraits).
- [ ] **Step 3: Commit approved panel + workflow.**

### Task 2: Page 1 remainder (P1.2–P1.4)

**Files:** `workflows/flux3_s1_p12.json`, `.../p13.json`, `.../p14.json`; outputs `sessions/session01/panel12_dragon.png`, `panel13_hooded.png`, `panel14_reveal.png`.

- [ ] **Step 1: Generate all three** — P1.2 Marigold startled amid staring patrons (fixed Marigold seed #1); P1.3 corner table hooded figure, face hidden by mist/pipe smoke, green-filigree cloak, soup bowl (NOT Biggins-suited); P1.4 same figure hood down, kindly bearded old gentleman laughing, merchant cloak (NOT Biggins — no suit, no watch chain; verify against approved_biggins_reference).
- [ ] **Step 2: Count figures per panel vs script; present all three; verdict.**
- [ ] **Step 3: Commit approved panels + workflows.**

### Task 3: Page 2 (P2.1–P2.4, job board)

**Files:** 4 workflows/outputs under `sessions/session01/` (`panel21_tip.png`, `panel22_board.png`, `panel23_quest.png`, `panel24_unpaid.png`).

- [ ] **Step 1: Generate** — P2.1 Marigold (same seed) pointing outside, Sammy silhouette in kitchen; P2.2 crowded job board with kitten poster prominent, Vadania overwhelmed foreground; P2.3 Keechwah pulling cat poster revealing weathered 600-gold posting behind; P2.4 party hurrying out door, Marigold waving, empty mugs, Sammy noticing (SFX BANG).
- [ ] **Step 2: Figure-count check; present; verdict.**
- [ ] **Step 3: Commit.**

### Task 4: Page 3 (P3.1–P3.5, Sammy + guards + tattoos)

**Files:** 5 workflows/outputs (`panel31_sammy.png` … `panel35_tattoo.png`).

- [ ] **Step 1: Generate** — P3.1 Sammy (adult male cook, apron, bill/menu high, shouting) bursting through inn doors, market crowd; P3.2 guards swords drawn advancing, merchants at stalls; P3.3 Marigold (same seed) hand out for coins, smacking Sammy; P3.4 Rocketcandy front-center crest out, guards sheathing; P3.5 macro close-up of guard inner wrist with geometric diamond sigil tattoo (no faces — detail shot).
- [ ] **Step 2: Figure-count check; present; verdict.**
- [ ] **Step 3: Commit.**

### Task 5: Page 4 (P4.1–P4.4, Chip's store — split thread)

**Files:** 4-5 workflows/outputs (`panel41_store.png` … `panel44_sweep.png`).

- [ ] **Step 1: Generate P4.1 FIRST, stop for verdict** — Chip + Water Bear (single owlbear: grizzly body + owl head + ruff, no wings, no second head) entering general store, bear bumping shelf, vase wobbling. Owlbear composition is the risk; do not batch the rest behind it.
- [ ] **Step 2: Generate P4.2–P4.4** — guards cornering Chip (sword under chin), proprietor with cast-iron pan mid-swing (BONK), leg sweep + hogtied guards in cellar. Mark all with `Meanwhile...` banner text in panels.json.
- [ ] **Step 3: Figure/creature-count check (one bear, three guards, no extra heads/wings); present; verdict.**
- [ ] **Step 4: Commit.**

### Task 6: Page 5 (P5.1–P5.5, mansion + apothecary)

**Files:** 5 workflows/outputs (`panel51_mansion.png` … `panel55_apothecary.png`).

- [ ] **Step 1: Generate** — P5.1 gated marble mansion, peacock, snooty butler; P5.2 mismatched opulent foyer, Vadania smirking; P5.3 Keechwah reaching for absent patron magic (visual: empty hand, faint whisper); P5.4 Lady Filvenar entrance (fire-red Celtic-knot braid, gray eyes, pirate shirt + corset — distinct from Lilly); P5.5 Chip entering Colorful Creations apothecary, giddy owner (Meanwhile-thread banner).
- [ ] **Step 2: Figure-count check; Filvenar-vs-Lilly distinctness check; present; verdict.**
- [ ] **Step 3: Commit.**

### Task 7: Assembly (prologue + personae + full comic HTML + log)

**Files:**
- Modify/create: `comics/session01.html` (full rebuild), `sessions/session01/panels.json`.

**Interfaces:**
- Consumes: all approved panels (Tasks 1-6 + P1.1), six approved portraits, approved lineup v2, narration/quotes from `script.md`.

- [ ] **Step 1: Prologue page** — six mini-panels reusing approved portraits, each with one journal/downtime line from the transcript (Rocketcandy's chronicle, Shade's not-diary, Gulgrim's meditation, Keechwah's study, Chip's star maps, Vadania's return). No generations.
- [ ] **Step 2: Dramatis personae** — approved lineup v2 image + one-line role per character from sheet facts.
- [ ] **Step 3: Comic body** — all panels in script order with narration boxes + attributed quotes from `script.md`; `Meanwhile...` banners on P4.1–P4.4 and P5.5; d20 result badges on roll panels (Vadania's 1, Keechwah's 17, Chip's grapple 16-vs-9, butler's 4 psychic); SFX per script.
- [ ] **Step 4: Quote traceability check** — every speech line maps to a transcript/script line; list any narration bridges added.
- [ ] **Step 5: panels.json** — one entry per shipped image (prompt, seed, model, file); assert count matches image files.
- [ ] **Step 6: Present HTML + quote map; verdict. Commit.**
