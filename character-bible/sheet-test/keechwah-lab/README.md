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

## Verdicts

- Batch 3 (human verdict 2026-11-02): all twenty read as tiefling, none
  really good. Two defects: horns look tacked-on rather than grown, and
  the red still needs to go lighter. Batch 4 takes skin first, horns next
  (one variable per batch).
