# HANDOFF — finish Session 1 fixes (fresh session brief)

## Mission
Complete the independent reviewer's fix list for `comics/session01.html`, then publish. Prior session hit provider request-size errors from image-bloated context: **one image read per turn max, never re-read an image, keep turns small.**

## State (all committed on main)
- Lettering fixes applied (commit 515786b): Ben/Marigold/Thumba speaker labels, Butler/Filvenar lines sourced, Keechwah trim, Sammy named, Chip absence noted, ARad gloss, pan clarity, hogtie honesty.
- Tattoo wording unified to "geometric diamond sigil tattoo of fine interlocking lines" in `flux3_s1_docks.json`, `flux3_s1_docksgate.json`, `flux3_s1_p35.json` — RE-ROLLS NOT YET RUN.
- Panels.json log + verify scripts: `C:\Users\Andrew\AppData\Local\Temp\opencode\build_panels_json.py`, `verify_comic.py`.

## Remaining work, in order
1. **Re-roll tattoo trio** (workflows above, same seeds) → verify single sigil design reads the same → save over `panel0_docks.png`, `panel0b_gate.png`, `panel35_tattoo.png`.
2. **Marigold P3.3 recast** via multiref (`workflows/base_flux3_multiref.json`, image `multiref_marigold.png` already on ComfyUI input) with halfling-small wording → save over `panel33_marigold.png`.
3. **P4.2 Roland recast** via multiref (`multiref_roland.png` on server) → save over `panel42_shakedown.png`.
4. **P3.2 de-clone** (four distinct guard faces) → save over `panel32_swords.png`.
5. **Hogtie actual binding** (visible wrist/ankle ropes) → save over `panel44_hogtied.png`.
6. **Dead-magic empty hand** (or accept flicker caption) → `panel53_deadmagic.png`.
7. **Dragon-flee background** (patrons fleeing) → `panel12_dragon.png`.
8. Re-run `verify_comic.py`, update `panels.json` entries for re-rolled panels, commit each approval.
9. Send the cold reader back for the final gate before publishing.

## Standing rules (do not renegotiate)
- Bible/director are locked; user approves new looks + canon only.
- Quote discipline: speech must trace to transcript lines (`sessions/session01/transcript.txt`).
- ComfyUI at 127.0.0.1:8188 (== 10.13.37.88, same box). Base graphs: `workflows/base_flux3.json` (text), `workflows/base_flux3_multiref.json` (portrait refs; single-ref proven).
- User grants: auto re-roll on spotted defects; escalate only canon decisions, story confusion, defects surviving two re-rolls.
- A second session commits lab/sheet-test work on main — coordinate on shared paths; its work is independent.

## Key prompt lessons (paid for in full)
- Absence by omission beats negation (never "no X", just don't mention X).
- Word colors onto nouns ("deep red skin, black hair", never "red tiefling").
- Same-seed re-rolls converge; fresh seed + full restatement for count/composition problems.
- Full locked identifiers per figure; countable compositions (rows, not piles).
