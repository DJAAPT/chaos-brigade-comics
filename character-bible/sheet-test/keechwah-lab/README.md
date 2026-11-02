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

## Verdicts

- (pending batch-1 review)
