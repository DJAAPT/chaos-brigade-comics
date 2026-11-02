# Keechwah Lab — versioned batches

Same protocol as the Shade lab (`../shade-lab/README.md`): never
overwrite — every generation snapshots to `batches/batch<N>/` with its
`prompts.json`, `descriptions.md`, and `img/`. Top-level `img/` +
`prompts.json` always hold the LATEST batch. Builder:
`scripts/build_lab.py --slug keechwah`. Workflows live under the
`keechwahlab_` prefix. Verify with
`--roster keechwah_k01 .. keechwah_k04` (batch 1).

## Batch history

| Batch | Wording vs previous | Seeds |
|---|---|---|
| batch1 | Baseline: Arm B Keechwah block verbatim; k01 uses seed 424242 = byte-identical reproduction of Arm C's Keechwah (control) | keechwah_k01–k04 (424242, 424243, 777001, 424244) |
| batch2 | Human-first skin per DDB's own ordering: `deep red skin` → `dark bronze skin with a deep red undertone` (batch 1 read full-demon) | same k01–k04 |
| batch3 | 20-seed survey on the batch-2 block (master list seed 20261104, disjoint from all prior) — keeper/feature read | keechwah_r01–r20 |
| batch4 | One step lighter still: `warm bronze-tan skin with a faint red cast` (batch 3 verdict: all tiefling, none great; horns tacked-on, red still heavy) | same k01–k04 |
| batch5 | Horns grown, not stuck on: `large curved horns growing naturally from his temples and emerging through his hair` (batch-4 skin held, k03's leftover red reads seed-specific) | same k01–k04 |
| batch6 | 20-seed survey on the batch-5 block (master list seed 20261105, disjoint from all prior) — keeper/horn read | keechwah_r01–r20 |
| batch7 | Burial made explicit from the gallery ref: `rising from the crown of his skull with bases buried deep in his thick curly hair` (keepers r10/r13 won by accident of this; rest of ref look NOT adopted) | same k01–k04 |
| batch8 | 20-seed survey on the batch-7 block (master list seed 20261106, disjoint from all prior) — keeper/horn read | keechwah_r01–r20 |
| batch9 | Solid-not-glowing eyes: `glowing purple` → `solid purple eyes with no visible sclera or pupil`, hue kept (canon fix, batch-8 keepers r07/r10) | same k01–k04 |
| batch10 | Matte finish: batch-9 verdict showed the glow surviving as purple spill onto the face, so `matte` joins as a positive finish word | same k01–k04 |
| batch11 | 20-seed survey on the batch-10 block (master list seed 20261107, disjoint from all prior) — keeper/eye read | keechwah_r01–r20 |
| batch12 | Replication survey: frozen batch-10 wording × 20 new seeds (master list 20261108) — pass bar is a keeper rate near batch 11's | keechwah_r01–r20 (new ladder) |

## Verdicts

- Batch 3 (human verdict 2026-11-02): all twenty read as tiefling, none
  really good. Two defects: horns look tacked-on rather than grown, and
  the red still needs to go lighter. Batch 4 takes skin first, horns next
  (one variable per batch).
- Batch 4 (human verdict): better, k03 still a little too red — reads
  seed-specific, not wording. Skin locked at the bronze-tan cast.
- Batch 5 (human verdict 2026-11-02): k03 has the best horns of the batch
  (seed 777001 again), rest look off — wording proven on one seed, survey
  next for hit rate + keepers.
- Batch 6 (human verdict): keepers r10 (seed 1342234658) + r13 — won by
  burying the horns in the hair; gallery ref confirms the mechanism.
- Batch 8 (human verdict 2026-11-02): keepers r07 (1743082206) + r10
  (106986660). New defect: eyes must read solid single-color, NOT
  glowing — normal eye shape, one color, no sclera/pupil split (canon).
  Batch 9 fixes the finish, keeps the hue.
- Batch 9 (human verdict 2026-11-02): k03 best overall (eyes + decent
  horns); k02 liked but the glow survives as purple spill onto the face
  around the eye, not in the eye itself; k01/k04 horns bad. Batch 10
  targets the finish with `matte`.
- Batch 10 (human verdict): k03 best of the bunch, right mix of
  everything — surveying the batch-10 wording 20 wide next.
- Batch 11 (agent review 2026-11-02, CORRECTED by human): agent's ~8-keeper
  count was overgenerous — human's true keepers are r07 + r10 only.
  Agent favorite r13 demoted: its horns render GOLD, which reads wrong.
  Finding: horn COLOR is unspecified in every prompt so far (canon and
  gallery ref both show dark horns) — new variable for the next batch.
- Batch 12 (human verdict 2026-11-02): standout r07 (seed 1826299574),
  but many bad — horns still addon-like, eyes still bad on most. The
  batch-11 hit rate did NOT replicate; wording not yet stable.
- Batch 4 (human verdict): better, k03 still a little too red — reads
  seed-specific, not wording. Skin locked at the bronze-tan cast.
- Batch 5 (human verdict 2026-11-02): k03 has the best horns of the batch
  (seed 777001 again), rest look off — wording proven on one seed, survey
  next for hit rate + keepers.
- Batch 6 (human verdict): keepers r10 (seed 1342234658) + r13 — won by
  burying the horns in the hair; gallery ref confirms the mechanism.
- Batch 8 (human verdict 2026-11-02): keepers r07 (1743082206) + r10
  (106986660). New defect: eyes must read solid single-color, NOT
  glowing — normal eye shape, one color, no sclera/pupil split (canon).
  Batch 9 fixes the finish, keeps the hue.
- Batch 9 (human verdict 2026-11-02): k03 best overall (eyes + decent
  horns); k02 liked but the glow survives as purple spill onto the face
  around the eye, not in the eye itself; k01/k04 horns bad. Batch 10
  targets the finish with `matte`.
- Batch 4 (human verdict): better, k03 still a little too red — reads
  seed-specific, not wording. Skin locked at the bronze-tan cast.
- Batch 5 (human verdict 2026-11-02): k03 has the best horns of the batch
  (seed 777001 again), rest look off — wording proven on one seed, survey
  next for hit rate + keepers.
- Batch 6 (human verdict): keepers r10 (seed 1342234658) + r13 — won by
  burying the horns in the hair; gallery ref confirms the mechanism.
- Batch 8 (human verdict 2026-11-02): keepers r07 (1743082206) + r10
  (106986660). New defect: eyes must read solid single-color, NOT
  glowing — normal eye shape, one color, no sclera/pupil split (canon).
  Batch 9 fixes the finish, keeps the hue.
- Batch 4 (human verdict): better, k03 still a little too red — reads
  seed-specific, not wording. Skin locked at the bronze-tan cast.
- Batch 5 (human verdict 2026-11-02): k03 has the best horns of the batch
  (seed 777001 again), rest look off — wording proven on one seed, survey
  next for hit rate + keepers.
- Batch 6 (human verdict 2026-11-02): keepers r10 + r13 — won by burying
  the horns in the hair. Gallery ref `Keechwah_and_Lilly_bonding.png`
  confirms the target: horns rising from the crown with bases swallowed
  by the hair mass, horn + hair reading as one structure (rest of that
  image's look NOT adopted). Batch 7 makes the burial explicit.
- Batch 4 (human verdict): better, k03 still a little too red — reads
  seed-specific, not wording. Skin locked at the bronze-tan cast.
- Batch 5 (human verdict 2026-11-02): k03 has the best horns of the batch
  (seed 777001 again), rest look off — wording proven on one seed, survey
  next for hit rate + keepers.
