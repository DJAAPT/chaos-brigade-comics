# Flux3-Only Pipeline Switch — Design (short)

**Status:** DRAFT — awaiting user approval (2026-11-01)
**Approaches:** see bottom; user picked Approach B in conversation.

## Intent

All comic image generation runs Flux3 Image Klein. No Flux2 path is maintained anywhere in the process docs or workflows. This unblocks the user's sequence: switch process → re-test Shade against the bible under Flux3 → approve remaining characters → regenerate session 1.

## Decisions (user, 2026-11-01)

- **Flux3 only, no Flux2 backup** — docs and workflows reference Flux3; the one Flux2 workflow file is deleted.
- **Multi-reference stays parked** — the multiref graphs were someone else's experiment, not user-validated. Pipeline stays text-only with locked prompt chunks; Flux3 is the renderer, nothing else changes about prompt strategy.
- **Commits go to main** (standing consent from the shade-identity-fix plan, same session/repo).
- **Rig (pinned, already verified in-repo):** unet `flux3-image-klein-nvfp4.safetensors` (weight_dtype default), CLIP `qwen3vl_4b_int8_convrot.safetensors` type `flux3`, VAE `flux2-vae.safetensors` (reused by Flux3), KSampler 15 steps / cfg 1.0 / er_sde / simple, latent 1344×768. Source graph: `workflows/bibleref_a_origseed.json` (verified text-only: 8 nodes, one populated prompt, one empty negative).

## Changes

1. **`README.md`** — line 2: ComfyUI address described as this machine (`10.13.37.88` = its own LAN IP; loopback also works), engine Flux3 Klein nvfp4. Line 3: base workflow = `workflows/base_flux3.json` with the full rig spelled out. Line 8: stage 3 heading Flux 2 → Flux 3. Nothing else in README mentions Flux2; quickstart's `comfy.exe` path (stale, from David's machine) is out of scope and untouched.
2. **`character-bible/bible.md:7`** — "Flux 2 has no identity memory between prompts" → "Flux 3 (Klein, text-only) has no identity memory between prompts". Rest of the drift section (including the future identity-pass note) unchanged. The `flux2-vae.safetensors` filename stays wherever it appears — it is Flux3's VAE too.
3. **`scene-director/director.md:37`** — `workflows/base_flux2.json` → `workflows/base_flux3.json`.
4. **Create `workflows/base_flux3.json`** — copy of `bibleref_a_origseed.json` with the populated `CLIPTextEncode` node's `inputs.text` set to the literal sentinel `{{PROMPT}}`; every other node byte-identical (sampler, steps, resolution, seed untouched). Same contract the sheet-test plan's Task 1 defines, so that never-executed plan stays compatible if run later.
5. **Delete `workflows/flux2_detail_closeup.json`** — untracked, unrecoverable; approved via Approach B. Its output PNG stays in `sessions/flux3-test/` as test history. All other Flux2-era *outputs* stay; Flux2 *models* on disk stay (not part of the process).
6. **`FLUX3-SETUP.md`** — status block becomes COMPLETE/Flux3-only; download checklist retained for re-install.

## Non-goals

- Multi-reference identity pass (parked, user decision).
- Shade re-validation under Flux3 — next step, separate work, needs the user's eye.
- Remaining character approvals, session 1 regeneration.
- README quickstart modernization; removing Flux2 model files from `C:\DEV\ComfyUI\models`.

## Verification (tests, RED→GREEN per task)

- `base_flux3.json` exists; content asserts unet/clip/type/vae/steps/cfg/width values above AND exactly one text node == `{{PROMPT}}` (the other empty).
- `validate_workflow(workflows/base_flux3.json)` against live Comfy → `valid: true`.
- Grep README + bible + director for `Flux ?2(?!-vae)|base_flux2|fp8mixed|mistral fp8` → 0 hits (lookahead keeps the legit `flux2-vae` filename).
- `Test-Path workflows/flux2_detail_closeup.json` → False.
- `FLUX3-SETUP.md` contains the COMPLETE status.

## Approaches considered

- **A — process swap only:** update the three docs, pin base workflow, leave the unused Flux2 workflow file in place. Cheapest; leaves a contradicted artifact behind.
- **B — swap + purge (chosen):** A plus deleting the Flux2 baseline workflow and marking the setup doc complete. Matches the user's "only Flux 3"; only real cost is the unrecoverable untracked file, whose output PNG survives as history.
