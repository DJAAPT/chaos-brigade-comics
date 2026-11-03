# Lineup Lab — Scene-First Identity Spike Design (2026-11-03)

## Intent and why
Prove we can hold core-character likeness by generating the scene first, then inserting characters one-by-one — starting with a police-lineup-style wall + Shade alone — because all-together text-to-image re-rolls faces and bleeds them in groups.

## Goals
- Batch 1 proves: empty lineup wall (no people, no height marks, heights obvious by stature) + Shade inserted from `approved_shade_reference.png` is instantly recognizable cold on hair, face, vest, 3ft stature.
- Self-contained `character-bible/lineup-lab/` that never touches `sheet-test/` or other labs; batch snapshots make every run comparable.
- Repeatable path to 6-person lineup keeping everyone recognizable.

## Non-goals
- No full automation, no comic HTML, no transcript plumbing in this spike.
- No new prompt wording to fix identity; wording frozen.
- No 6-person image in batch 1.

## Anti-goals
- Tuning wording to fix bleed; accepting "close enough" likeness.
- Overwriting prior batches; a run without a snapshot.

## Constraints
- Use only approved refs (`character-bible/approved_*_reference.png`); Shade ref is `approved_shade_reference.png`.
- Flux3 Klein only: `flux3-image-klein-nvfp4.safetensors` + `qwen3vl_4b_int8_convrot.safetensors` + `flux2-vae.safetensors`; 1344x768 to match labs.
- Local ComfyUI `http://127.0.0.1:8188` (LAN `10.13.37.88` also works); free local nodes only (`ReferenceMultiLatent`, `VAEEncodeForInpaint` available; no partner-API nodes).
- No height marks; stature gap must read without them.

## Approaches considered
1. All-together with visual refs (`ReferenceMultiLatent`, 1-6 refs in one pass) — fastest, but face bleed killed the 6-person lineup; thrown out for groups per human decision.
2. Scene-first, cast one-by-one (chosen for this spike) — empty backdrop, then masked insert per character from approved pixels; best identity lock, heights controllable, more steps.
3. Hybrid (future) — solos all-together where they hold, groups scene-first; decided after spike.

## Parts decided
- New dir `character-bible/lineup-lab/` mirroring `sheet-test/*-lab/` ledger pattern: `README.md`, `descriptions.md`, `prompts.json` (latest), `img/` (latest), `batches/batch<N>/` snapshots, `slots.json` for positions.
- Batch 1 = empty wall + Shade alone; batch 2+ = add remaining five one at a time.

## Left to builder
- Backdrop prompt text, slot mask geometry, exact insert workflow JSON (ReferenceMultiLatent vs VAEEncodeForInpaint denoise value), seed ladder, verify gate thresholds.
