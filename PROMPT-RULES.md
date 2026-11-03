# Prompt Lab Rules — distilled from the Shade lab (14 batches, 64 images)

These rules override generic prompt advice wherever they conflict. Each
was established by controlled batches (same seeds, one wording variable),
not by theory. Full records live in `character-bible/sheet-test/`.

## Wording rules (Flux3 Klein, text-only, Qwen3-VL encoder)

1. **Name the species for scale, never name the ears.** The species word
   carries smallness AND the ear prior together (batch 12 vs 13 proved
   both directions). Ear words — adjectives, placement, anatomy nouns —
   only ever made ears worse across 11 batches. Hair-covering carries the
   ear constraint instead.
2. **Identity beats measurement.** Counterfactual identity sentences
   ("enlarged to six feet he would be indistinguishable from an ordinary
   human man") moved age/size where ratios (`one-seventh`), adjectives,
   and placement never did (batches 4–5).
3. **Bans are dead weight, not poison.** Batch 7 vs 8 (same seeds, bans
   present vs stripped): no worse, no better. Prompt space spent on
   `NOT`/`no` is better spent on positive anatomy. Keep bans out of new
   wording; leave existing locked-chunk bans alone unless testing them.
4. **Official species canon can feed the prior.** DDB halfling text
   ("diminutive", "appear relatively harmless") pushes the baby schema —
   quote canon selectively, never wholesale.
5. **Distilled Klein ignores negative prompts.** Empty negative node into
   a cfg-1.0 sampler: weighted negatives (`(large ears:1.6)`) have nowhere
   to execute. Relevant again only on the undistilled base model.
6. **External advice is guilty until proven innocent.** Two Gemini
   consults contributed real wins (ear anatomy nouns, ear-silence theory)
   alongside claims our batches had already falsified (numeric ratios) or
   our rig can't execute (negative weights, T5/CLIP tuning — our encoder
   is Qwen3-VL-4B). Adopt per-claim, test per-claim.

## Experiment protocol

7. **One variable per batch, same seeds.** Filename-to-filename comparison
   is the whole method; batches that change two things prove nothing.
8. **Controls first.** A `424242`-seeded entry reproducing the current
   best prompt isolates wording from seed luck (determinism verified:
   same prompt + seed + graph = hash-identical pixels).
9. **Some seeds are hostile, not informative.** 314159 failed every
   wording across 5 batches — retired, not chased. Distinguish cursed
   seeds (bad everywhere) from wording failures (bad on one batch) by
   comparing one seed across batches before iterating wording.
10. **Survey before concluding.** 4-seed batches kept missing keepers the
    20-seed surveys found (batch 9: 5/20, batch 14: 5/20). Hit-rate reads
    need N=20 with a recorded master seed list.
11. **Never overwrite.** Every generation snapshots to
    `<lab>/batches/batch<N>/` (`prompts.json` + `descriptions.md` +
    `img/`) **immediately after the run verifies, before any verdict** —
    the snapshot belongs to the run, not the review, so every batch stays
    comparable later; top-level `img/` is always the latest. All
    pre-batch-9 Shade images were recovered from git history — never
    again.
12. **Locked chunks stay verbatim unless the human approves a deviation.**
    Batch 12's chunk surgery was explicit, ledgered, and test-pinned as a
    deviation — the exception that proves the process.

## Standing decisions (2026-11-02)

- Shade pinned block: `character-bible/sheet-test/shade-lab/descriptions.md`
  (batch-13/14 text); approved seeds: 777001 + batch-14 q02/q07/q13/q17/q19.
- Shade approved ref: `character-bible/approved_shade_reference.png`
  (batch-14 q13, seed 1395696223).
- No scale objects in reference prompts (door/acorn declined twice).
- Frame + addendum constants are experiment infrastructure — change them
  only as their own arm, never inside a wording batch.
