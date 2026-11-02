# Shade Lab — versioned batches

**Rule going forward: never overwrite. Every generation is a new batch.**
The top-level `img/` + `prompts.json` always hold the LATEST batch (tooling
expects them there). Each completed batch is snapshotted under
`batches/batch<N>/` with its `prompts.json`, `descriptions.md`, and `img/`
so wording and pixels stay paired for side-by-side comparison. Workflows
for any batch are recoverable from git history (`workflows/shadelab_*` at
the batch commit); only the latest set lives in `workflows/`.

## Batch history

| Batch | Commit | Wording change vs previous | Seeds |
|---|---|---|---|
| batch1 | `269c5ae` | v1: Arm B block + "small adult, NOT a child" + scaled-down clause + four ear bans (descriptions from `f163c2e`) | 424242 / 424243 / 777001 / 314159 |
| batch2 | `9551f52` | Ratio-anchored clause: identical head-to-body and ear-to-head proportions, anti-chibi bans | same four |
| batch3 | `3339e44` | Ear-placement clause: ears tucked under hair, flat, below eye level, "no pointed tips" | same four |

Human verdicts so far: batch 2 `shade_s2` closest on head size; ears still
sticking out through batch 3.

**Locked base going forward (human, 2026-11-02): `shade_s2`, seed 777001 —
best head proportions in every batch. Future Shade iterations run on this
seed; wording carries forward from the latest batch unless noted.**

## Comparing batches

Same key across batches = same seed = wording-only delta
(e.g. `batches/batch2/img/shade_s2.png` vs
`batches/batch3/img/shade_s2.png`). `shade_s0` (seed 424242) additionally
controls against Arm C's `arm_c/img/shade.png`.
