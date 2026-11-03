# Batch 2 — true masked insert (method spike, uncommitted)

Goal: prove Shade can be painted INTO the actual batch-1 wall plate pixels,
not into a regenerated backdrop. Verdict on batch 1 stands: the
`wall_shade_s1` ReferenceMultiLatent-only workflow never loads the wall —
it re-renders a lookalike backdrop, so it does not count as scene-first.

## Runs (all: seed 777001, same prompt + ref as batch 1, wall plate `img/wall_empty.png`)

| Run | Workflow | Change vs previous | Result |
|---|---|---|---|
| b2 | `lineuplab_b2_shade_masked.json` | VAEEncode wall + SetLatentNoiseMask (slot x420-760), denoise 0.75 | FAIL — clean wall, no figure. Partial denoise from wall pixels can't form the figure |
| b2b | `lineuplab_b2b_shade_masked.json` | denoise 0.75 → 1.0 only | PARTIAL — Shade appears in the real plate, wall preserved, but mask too narrow: figure clipped at right edge |
| b2c | `lineuplab_b2c_shade_wide.json` | mask widened (x380-880) only | PASS — full unclipped Shade in the real plate, likeness holds vs approved ref |

## Recipe (pinned for batch 3+)

LoadImage(wall) → VAEEncode → SetLatentNoiseMask(slot mask) → KSampler(denoise 1.0,
positive/negative from ReferenceMultiLatent(ref image + prompt)) → VAEDecode.
Distilled Klein, 15 steps / cfg 1.0 / er_sde / simple. Mask PNGs live beside this note.

## Contents

- `img/`: b2 (fail), b2b (clipped), b2c (keeper)
- `mask_shade_slot.png` (narrow, clips), `mask_shade_wide.png` (keeper geometry)
- The three workflow JSONs that produced them
- `prompts.json` + `descriptions.md`: carried over from batch 1 unchanged
  (no wording changed in this batch — method only)
