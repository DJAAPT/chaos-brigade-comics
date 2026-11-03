# Lineup Lab — scene-first identity spike

**Rule: never overwrite.** Top-level `img/` + `prompts.json` hold the LATEST batch.
Each run snapshots `prompts.json` + `descriptions.md` + `img/` to `batches/batch<N>/`
before any verdict. Workflows for a batch are recoverable from git history
(`workflows/lineuplab_*` at the batch commit); only the latest set lives in `workflows/`.

## Batch history

| Batch | Wording / method change vs previous | Seeds |
|---|---|---|
| batch1 | Empty neutral lineup wall (no people, no height marks) + Shade inserted from approved ref via masked reference workflow | wall 424242 / shade 777001 |
