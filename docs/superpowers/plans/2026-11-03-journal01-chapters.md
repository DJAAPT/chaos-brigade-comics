# Journal 01 Chapters 4–8 + Art Lock — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Native execution (writer implements
> directly in this session; voice consistency forbids farming prose to subagents).

**Goal:** Draft Chapters 4–8 of the Journal 01 manuscript (Marigold's rest → mansion
tag) and lock the art list, ready for the generation phase.

**Architecture:** Single manuscript file appended in chapter order; quote-trace check
against the transcript digest after drafting; commit once.

**Tech Stack:** Markdown manuscript in `docs/`; Flux3 multiref rig for later art.

**Spec:** `docs/chronicle-journal01-proposal.md` (§§6–13: chapter divisions, voice rules,
art/DM-note placements, open questions).

## Global Constraints

- Every speech line traces to a transcript line (proposal §2 digest + timestamps).
- Never invent an event, result, or motive; connective narration only.
- Ben first-person voice rules (proposal §5); DM notes sparing (proposal §11).
- No artwork or layouts in this phase — prose + locked lists only.
- Open questions (§12) are worked around, not answered: end Ch.7 at the back-door
  shove; "Water Bear" throughout with the Albert lampshade; "Thumba's shop" neutral
  wording; current cast spellings, normalized later.

## Review Focus

- A verbatim quote misremembered from the digest (check each against §2-quote list).
- A joke that requires D&D knowledge without in-narration context for outsiders.
- A DM note that punches down at a player rather than at the situation.
- A chapter ending without a forward pull (each must hand off to the next).
- Bronze-tan vs "deep red" Keechwah wording leaking in from old prompts (use neutral
  skin wording: "red" only where the transcript says it — the harbormaster scene is
  Journal-later; here: "tiefling" + horns, no color claims).

---

### Task 1: Draft Chapters 4b–6 (Marigold's rest, Kitten/600g, THIEVES!)

**Files:**
- Create: `docs/chronicle-journal01-chapters4-8.md` (Tasks 1–2 append to it)

**Interfaces:**
- Consumes: proposal §§2,4,6,11 (beats, quotes, chapters, DM notes).
- Produces: manuscript sections Ch.4b, Ch.5, Ch.6 with H2 headers.

- [ ] Step 1: Write Ch.4b (hooded stranger → reveal → apothecary round → board tip +
  Sammy ladle), ~500 words, ending on the walk to the board.
- [ ] Step 2: Write Ch.5 (VTT chaos, nat 1, Keechwah 17, hidden posting, north
  decision), ~500 words, ending on the commit to go north.
- [ ] Step 3: Write Ch.6 (crying merchants → Sammy → swords → 2g/4g → second clasp →
  guild theory → uniform tells), ~600 words, ending on the north walk + Bob Barker
  derail. Include DM notes: VTT, nat-1, Barker (max 3 across the three chapters).

### Task 2: Draft Chapters 7–8 (Chip solo, mansion)

**Files:**
- Modify: `docs/chronicle-journal01-chapters4-8.md` (append Ch.7, Ch.8)

**Interfaces:**
- Consumes: same as Task 1.
- Produces: manuscript sections Ch.7 (~800 words), Ch.8 (~700 words) + hook line.

- [ ] Step 1: Write Ch.7 as one block chapter (ruins → vase → slur → lie → sword-chin
  → 40g → pouch → pan → grapple → star tattoo → hogtie ball → Thumba note →
  back-door shove with gap lampshade). Include DM notes: slur-translation, Albert.
- [ ] Step 2: Write Ch.8 (foyer → roast → Mockery + "I hate that" → blindness → d4
  fail → whisper → patron-absent speech → Filvenar full entrance → bell/tag hook
  for Journal 02). Include DM notes: Mockery review, foyer blindness.
- [ ] Step 3: Quote-trace pass — every quoted line checked against the digest's
  verbatim list; fix or cut any that fail.
- [ ] Step 4: Commit (`docs/chronicle-journal01-chapters4-8.md` + plan file).

### Task 3: Lock the art list

- [ ] Step 1: Confirm proposal §9 (12 plates) + §10 (5 sequences) stand unchanged
  against the drafted chapters; record any swap with reason in the manuscript file's
  Art Lock appendix. No generations — lock only.
