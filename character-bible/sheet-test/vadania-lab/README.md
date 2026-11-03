# Vadania Lab — versioned batches

Same protocol as the Shade, Keechwah, and Gulgrim labs
(`../shade-lab/README.md`, `../keechwah-lab/README.md`,
`../gulgrim-lab/README.md`): never overwrite — every generation
snapshots to `batches/batch<N>/` with its `prompts.json`,
`descriptions.md`, and `img/` immediately after verify, before any
verdict. Top-level `img/` + `prompts.json` always hold the LATEST batch.
Builder: `scripts/build_lab.py --slug vadania --keys ...` (the `--keys`
flag is REQUIRED — defaults are shade keys). Workflows live under the
`vadanialab_` prefix. Verify with
`--roster vadania_g01 .. vadania_g04` (batch 1).

Baseline block is the Arm B Vadania block verbatim; seed ladder is the
control set `424242 / 424243 / 777001 / 424244` (424242 = byte-identical
Arm C reproduction; hostile seed 314159 already retired by the Shade
lab, so 424244 takes its slot — note 424244 was retired *for Gulgrim*
over grey hands but is clean on Keechwah; its Vadania behavior is new
evidence either way). Approved reference for judging:
`character-bible/approved_vadania_reference.png`.

## Judging baselines (apply to every verdict)

- **Canon:** `character-bible/bible.md` — Vadania Amakiir section:
  NEVER female, dress, blonde hair (brown per sheet), "long blonde
  woman in green" misrender, or duplicate Vadania as barmaid. Weapons:
  ornate Monster Hunter's Longbow +1 + twin shortswords (longbow on
  back, shortswords at hips). Blunt/direct, steady gaze, never soft or
  smiling.
- **Approved look:** `character-bible/approved_vadania_reference.png`
  (approved 2026-11-02, Flux3 v1) — face, expression, and gear are the
  target.

## Batch history

| Batch | Wording vs previous | Seeds |
|---|---|---|
| batch1 | Baseline: Arm B Vadania block verbatim — snapshot: `batches/batch1/` | vadania_g01–g04 (424242, 424243, 777001, 424244) |

## Verdicts

_(pending batch 1)_
