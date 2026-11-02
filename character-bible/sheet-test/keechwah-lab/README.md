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
| batch13 | Horn color pinned from both approved refs: `large curved bronze-brown horns` (open color drifted to gold/red); burial + matte + skin frozen | same k01–k04 |
| batch14 | Horn posture: `rising upright side by side` (batch-13 verdict split the defects — k01 splayed wide, k04 oversized; posture is word-addressable, size is not) | same k01–k04 |
| batch15 | 20-seed survey on the batch-14 block (master list seed 20261109, disjoint from all prior) — hunting k03's horns + k04's eyes in one frame | keechwah_r01–r20 |
| batch16 | Geometry over anatomy: `solid matte purple spheres instead of eyes` (batch-15 verdict — horns done via survey, eyes need work everywhere) | same k01–k04 |
| batch16 verdict (agent review 2026-11-02) | Backfire: literal glowing orbs — bug eyes on all four (worst k03, plus sleeveless wardrobe drift there). Removing the word "eyes" also removed eyelids/shape context that made eyes read as eyes. Lesson: the eye APPARATUS (lids, almond shape) is load-bearing; only the iris fill wants replacing. | — |
| batch17 | Lidded eyes with iris fill: apparatus kept, only the fill replaced (batch-16 lesson) | same k01-k04 |
| batch18 | 20-seed survey on the batch-17 block (master list seed 20261110) - purple-hold rate read | keechwah_r01-r20 |
| batch19 | Robe closure specified (bare-chest drift recurred batches 11+17) + 10-seed eye verification on the batch-17 block | keechwah_r01-r10 (new ladder) |
| batch19 verdict (human 2026-11-02) | FRAMING REGRESSION: r04 waist-up crop, r07 shin-cut - frame clause ignored on 2 of 10. Suspect: new 'worn closed over the chest' pulls composition toward the torso. Batch 20 tests causality: batch-17 block (no robe phrase) x the same 2 seeds. | - |
| batch17 verdict (agent review 2026-11-02) | Lids fixed the orbs everywhere - no bug eyes on any of the four. Purple held on k01/k03/k04, failed on k02 (blue-gray eyes). k04 best full package (lidded purple eyes, rooted bronze horns, closed robe, goatee, tail). k03 good face but bare-chest drift again. | - |
| batch17 verdict (human 2026-11-02) | k04 closest but the only one that kept purple - k01-k03 tossed the entire iris replacement (normal/dark eyes). Purple itself is seed-fragile, not just the finish. Batch 18 surveys the batch-17 block 20 wide for purple-holders. | - |

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
- Batch 11 (agent review, CORRECTED by human): true keepers r07 + r10
  only; r13 demoted on gold horns. Horn color unspecified anywhere —
  batch 13 pins bronze-brown from both approved refs.
- Batch 12 (human verdict 2026-11-02): standout r07 (1826299574), many
  bad — replication did not hold; wording not yet stable.
- Batch 13 (human verdict 2026-11-02): k02 + k03 good; k04's horns too
  large (size unspecified anywhere — seed noise unless it recurs);
  k01's horns split wide apart (posture). Batch 14 takes posture:
  upright + side-by-side.
- Batch 14 (human verdict 2026-11-02): k03 best horns, k04 best eyes,
  k01/k02 wrong on both — no single image complete. Batch 15 surveys
  the batch-14 wording 20 wide hunting the combination.
- Batch 15 (human verdict 2026-11-02): WAY better and more consistent —
  most have good horns. Eyes still need work on all of them. Batch 16
  tests geometry-over-anatomy: solid matte purple spheres instead of eyes.
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
