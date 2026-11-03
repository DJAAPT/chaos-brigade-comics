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

## Batch history

| Batch | Wording vs previous | Seeds |
|---|---|---|
| batch1 | Baseline: Arm B Gulgrim block verbatim — snapshot: `batches/batch1/` | gulgrim_g01–g04 (424242, 424243, 777001, 424244) |

## Verdicts

_(pending batch 1)_
