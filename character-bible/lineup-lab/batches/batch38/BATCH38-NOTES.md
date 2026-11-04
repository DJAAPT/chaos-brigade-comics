# Batch 38 — two-ref companions + Gulgrim hairy-helmet pivot

## Two-ref companions (main 7)
All approved refs carry embedded ComfyUI prompts+seeds. Companions built from each ref's own graph + seed, framing swapped:
- Full-bodies from waist-up seeds (1857761984156622644): vadania, chip, rocketcandy, keechwah, lilly (r3 pleated skirt fix approved)
- Closeups from full-body seeds: gulgrim (superseded by pivot below), shade r3 (approved, sly closed-mouth)
- Naming (pending user approval to execute): current waist-ups -> approved_<slug>_closeup.png, new full-bodies take approved_<slug>_reference.png. NOT DONE YET.

## Gulgrim pivot (James): bald/white -> hairy black helmet dwarf
Seeds: 777001 (original) + fresh 6472508315 / 7976038896 / 8342583591 / 1490431410 / 4620677048.
- LOCKED full-body: b38_gulgrim_fb_noweapon.png (seed 777001) — black masses, cheek helm, angular bemused, no weapon (warhammer doubles, reintroduce in scenes only).
- LOCKED closeup: b38_gulgrim_closeup_final5.png (seed 777001) — calm heavy-lidded, one brow lifted.
- Live as approved_gulgrim_reference.png / approved_gulgrim_closeup.png. Bald retired to approved_gulgrim_reference_bald_retired.png. Bible chunk rewritten. ComfyUI inputs re-copied + SHA-verified.
- Findings: (1) dropping no-oversized-head/no-large-head/no-bobblehead bans shrank the head on same seed — bans may actively hurt here, not just dead weight (single-seed observation, needs controls before touching PROMPT-RULES rule 3). (2) external "hill dwarf inflates head" claim FALSIFIED on seed 7976038896 (dropping it made head larger). (3) Marthammor Du symbol verified: upright mace in front of a tall boot (FR wiki); Gemini's "boot on staff" was wrong. (4) chain-replacing prompt text across builds silently no-ops — always assert replacement applied (bit us twice: r3 dupe + calm-file typo).
