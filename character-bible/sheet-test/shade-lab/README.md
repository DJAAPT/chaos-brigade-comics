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
| batch4 | _(this commit)_ | Head-ratio anchor: "head one-seventh of total body height, small adult head" — pass criterion is correct head size on **all four seeds**, not just s2 | same four |
| batch5 | _(this commit)_ | Identity over measurement: dead 1:7 ratio swapped for counterfactual ("full-grown man who happens to stand three feet tall, enlarged to six feet indistinguishable from an ordinary human man") + explicit NOT a baby / NOT a toddler bans (batch 4's s3 was a baby with a giant head) | same four |
| batch6 | _(this commit)_ | Seed generalization, wording frozen at batch 5: s2 control (777001) + three historic S1 seeds; s2 re-render hash-identical to batch 5 = pipeline deterministic | shade_s2, shade_s4/5/6 (1857761984156622644, 6120004243239096470, 8620240391160718909) |
| batch7 | _(this commit)_ | Ear-anatomy positives from the Gemini consult (pinned-flat skull, zero flair, small skull, sleek proportions), bans KEPT — isolates the new positives | same s2/s4/s5/s6 |
| batch8 | _(this commit)_ | Ban-strip test of Gemini's backfire claim: block-level NOT/no bans removed (chunk "no beard" + addendum "no shield" stay: verbatim + frame contract) — decisive pair vs batch 7, same seeds | same s2/s4/s5/s6 |
| batch9 | _(this commit)_ | 20-seed survey on the ban-free block (master list seed 20261102): hit-rate read on the best wording so far | shade_r01–r20 (fixed random list in `tests/test_shadelab.py`) |
| batch10 | `5ce6e45` | Gemini-merge additions (species skin, sideburns, tighter ear phrasing), ban-free kept, on batch-6 seeds — s2 is a three-way control (batches 6/8/10 wording × seed 777001) | shade_s2/s4/s5/s6 |
| batch11 | `cf73594` | Ear-silence test: added clause names no ears (only the locked chunk may); hair-covering carries the constraint | same s2/s4/s5/s6 |
| batch12 | _(this commit)_ | Halfling/ear-silence stress test (human-approved chunk deviation): locked chunk surgically edited — "halfling" out, ear phrases → hair-side wording; no `halfling`/`ear(s)` words anywhere | same s2/s4/s5/s6 |
| batch10 verdict (human + agent review, 2026-11-02) | s2 best again (adult proportions, outfit right) but ears still protrude sideways; s4 reads teen/child; s5 still baby-giant-head; s6 grew a full beard against "no beard" and dropped the gray studio backdrop for white — ear wording moved nothing in any of the four | — |

Human verdicts so far: batch 2 `shade_s2` closest on head size; ears still
sticking out through batch 3. Batch 4: explicit 1:7 ratio changed nothing —
s2 still the only correct head size (s3 terrible) — numeric ratios don't
move this model; head-size wins remain seed lottery so far. Batch 5
(identity + anti-baby bans): s1 AND s2 both good head sizes, s0's age
reads much better (head still large), s3 still HUGE head + toddler
despite facial hair — identity language fixed age on 3/4, size on 2/4.
Batch 5 `shade_s2` (seed 777001): head size AND ears both good — **lab
winner and locked base**. All other seeds still show oversized ears;
s3 (314159) bad in every batch — retired as a hostile seed, not a
wording signal. Batch 6 (frozen batch-5 wording, new S1 seeds): heads
better on all of s2/s4/s5/s6, still slightly large on s4–s6 but far
from the old giant-head failures — wording generalizes; ears still open.
Batch 9 survey (20 random seeds, ban-free block): keepers are r07, r08,
r09, r11, r14 — 5 of 20 close to the target. Hit rate is real but low;
wording still the lever.
Batch 7 vs 8 (same seeds, bans present vs stripped): batch 8 not worse,
not much better — **bans retired as useless, not harmful; ban-free
wording (batch-8 block) is the base going forward**.

**Locked base going forward (human, 2026-11-02): `shade_s2`, seed 777001 —
best head proportions in every batch. Future Shade iterations run on this
seed; wording carries forward from the latest batch unless noted.**

## Comparing batches

Same key across batches = same seed = wording-only delta
(e.g. `batches/batch2/img/shade_s2.png` vs
`batches/batch3/img/shade_s2.png`). `shade_s0` (seed 424242) additionally
controls against Arm C's `arm_c/img/shade.png`.
