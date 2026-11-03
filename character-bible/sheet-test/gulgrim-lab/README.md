# Gulgrim Lab — versioned batches

Same protocol as the Shade and Keechwah labs (`../shade-lab/README.md`,
`../keechwah-lab/README.md`): never overwrite — every generation
snapshots to `batches/batch<N>/` with its `prompts.json`,
`descriptions.md`, and `img/`. Top-level `img/` + `prompts.json` always
hold the LATEST batch. Builder: `scripts/build_lab.py --slug gulgrim`.
Workflows live under the `gulgrimlab_` prefix. Verify with
`--roster gulgrim_g01 .. gulgrim_g04` (batch 1).

Baseline block is the Arm B Gulgrim block verbatim; seed ladder is the
control set `424242 / 424243 / 777001 / 424244` (424242 = byte-identical
Arm C reproduction; hostile seed 314159 already retired by the Shade
lab, so 424244 takes its slot). Approved reference for judging:
`character-bible/approved_gulgrim_reference.png`.

## Judging baselines (apply to every verdict)

- **Canon:** `character-bible/bible.md` — Gulgrim Frozenboots section:
  NEVER tall, thin, no-beard, or missing his heavy furs (furs stay on in
  every panel); warhammer beats the sheet's mace; holy symbol of
  Marthammor Du; Cleric 5 / Soldier canon (Mintarn → Neverwinter).
- **Approved look:** `character-bible/approved_gulgrim_reference.png`
  (approved 2026-11-02, Flux3 v1; **replaced 2026-11-03 by gulgrim-lab
  batch-5 g03, seed 777001** — bald, warhammer worn at hip) — face,
  gear, expression and frost boots are the target. The two divergences
  tracked during the lab are resolved: the lab wording converged with
  the old ref on baldness, and improved on it with a proper worn
  warhammer where the old ref gripped an axe-like head.

## Batch history

| Batch | Wording vs previous | Seeds |
|---|---|---|
| batch1 | Baseline: Arm B Gulgrim block verbatim — snapshot: `batches/batch1/` | gulgrim_g01–g04 (424242, 424243, 777001, 424244) |
| batch1 verdict (human 2026-11-03) | Furs/beard/stockiness/NEVER-list hold on all four; weapon fails everywhere (0/4 clean warhammer); g04 renders grey hands — kept in ladder pending batch-2 re-check | — |
| batch2 | Weapon worn, not gripped: bare `warhammer` → `his warhammer at his hip` (batch-1 verdict); head shape untouched — single variable — snapshot: `batches/batch2/` | same gulgrim_g01–g04 |
| batch2 verdict (agent review 2026-11-03, human pending) | Position fix works: **4/4 warhammers** (batch 1 was 0/4), zero axe drift, no improvised grips; NEVER-list clean, holy symbol on all four; g03 best again. **g04 grey hands persisted → recommend retire 424244, promote 424245** | — |
| batch3 | Seed retirement: 424244 out (grey hands under two wordings), **424245 in** at `gulgrim_g04`; wording frozen at the batch-2 block — snapshot: `batches/batch3/` | gulgrim_g01–g04 (424242, 424243, 777001, 424245) |
| batch4 | 20-seed survey on the frozen batch-2 block (hit-rate read; master list 20261121) — wording unchanged, ladder new — snapshot: `batches/batch4/` | gulgrim_r01–r20 |
| batch4 verdict (agent review 2026-11-03, human pending) | Solid keepers r01, r02, r06, r11, r13, r16 (6/20) + keepers-with-notes r03, r07, r09, r10, r12, r18, r20 (7/20) — better than shade's 5/20 survey baseline. Axe drift essentially dead (1 partial in 20, r17); 424244-style grey hands never recur (r05/r15 mild frosting only). New variables for later batches: **r08 bald + bare midriff on white backdrop** (hair on head is unspecified in the block — drift source), weapon duplication r13/r14, polearm read r04, belt/symbol gibberish text r03/r15 | — |
| batch5 | **Bald pinned:** human decision — `, broad long white beard,` → `, bald, broad long white beard,` (batch-4 survey drifted bald twice on unspecified head hair); warhammer clause untouched — snapshot: `batches/batch5/` | gulgrim_g01–g04 (424242, 424243, 777001, 424245) |
| batch5 verdict (agent review 2026-11-03, human pending) | One word, 4/4 bald — clean sweep on the control ladder, no partials. Everything else holds: warhammers at hip, NEVER-list clean, hands natural on all four (424245 stays clean), holy symbols present. g03 (777001) best again. Lab wording now converges with the approved ref on the two recorded divergences (bald ✓, worn warhammer ✓) — ref replacement candidate once the human confirms | — |
| batch5 verdict (human 2026-11-03) | **LOCKED: g03 is Gulgrim's new approved identity ref** — `character-bible/approved_gulgrim_reference.png` replaced (2026-11-03, Flux3 Klein, seed 777001); bible.md approved-ref line updated. Bald + worn warhammer now canon in pixels, matching the lab wording | — |

## Verdicts

- Batch 1 (human verdict 2026-11-03): base block holds — broad long
  white beard, heavy furs, frost-covered boots, stocky dwarf silhouette
  and NEVER-list clean on all four. **Weapon is the failure:** g01
  double-bit axe, g02 tiny hammer at hip, g03 lumpy maul, g04 axe-pick —
  not one clean warhammer from the bare word `warhammer`. **g04 (424244)
  renders grey hands** on the gripping hand; first evidence for this
  seed, NOT retired — batch 2 re-checks it under new grip wording before
  any seed verdict (PROMPT-RULES #9). 777001 (g03) strongest overall
  again, matching the other labs. **Batch 2 takes the weapon phrase.**
- Batch 2 (agent review 2026-11-03, human pending): the single variable
  did its job — warhammer reads on all four (batch 1: 0/4), zero axe
  heads anywhere, no improvised grips, hands free with arms clearly
  visible (frame addendum clean). Bible NEVER-list clean on all four;
  holy symbol present on all four. g03 (777001) best again — third
  strong batch running for that seed. Open items: g02's ornate silver
  hammer head and bare knees (both seed-consistent from batch 1), g04's
  weapon partly hidden behind belt pouches. **g04 (424244) grey hands
  PERSISTED under empty-hands wording — batch 1 gripping hand, batch 2
  both hands; same defect, two different wordings, other three seeds
  normal in both batches → seed-specific per PROMPT-RULES #9.
  Recommend retiring 424244 and promoting 424245 (verified disjoint
  from every recorded ladder) into `gulgrim_g04` for batch 3.**
  Approved-ref divergences unchanged: lab has white hair (ref is bald),
  worn warhammer (ref grips an axe-like head) — human to adjudicate.
