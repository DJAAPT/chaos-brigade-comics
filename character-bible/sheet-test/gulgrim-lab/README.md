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
  (approved 2026-11-02, Flux3 v1) — face, gear, expression and frost
  boots are the target. Known divergences for the human to adjudicate
  as batches progress: the ref is **bald** (all lab renders have white
  hair) and grips an **axe-like** weapon head-down (batch 2 moved to a
  worn warhammer — the lab may be intentionally improving on the ref).

## Batch history

| Batch | Wording vs previous | Seeds |
|---|---|---|
| batch1 | Baseline: Arm B Gulgrim block verbatim — snapshot: `batches/batch1/` | gulgrim_g01–g04 (424242, 424243, 777001, 424244) |
| batch1 verdict (human 2026-11-03) | Furs/beard/stockiness/NEVER-list hold on all four; weapon fails everywhere (0/4 clean warhammer); g04 renders grey hands — kept in ladder pending batch-2 re-check | — |
| batch2 | Weapon worn, not gripped: bare `warhammer` → `his warhammer at his hip` (batch-1 verdict); head shape untouched — single variable — snapshot: `batches/batch2/` | same gulgrim_g01–g04 |

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
