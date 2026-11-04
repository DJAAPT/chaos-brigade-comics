# Chaos Brigade Image Pipeline — Playbook (2026-11-03 and on)

How we generate consistent-character comic art. Proven across lineup-lab batches 1–32 and sessions/session01/v2. Follow this instead of re-deriving it.

## Stack (pinned)

- ComfyUI local at `http://127.0.0.1:8188` (LAN `10.13.37.88` also works).
- Models, exact files: `flux3-image-klein-nvfp4.safetensors` (diffusion),
  `qwen3vl_4b_int8_convrot.safetensors` (CLIP, type `flux3`),
  `flux2-vae.safetensors` (VAE). No Flux2 for generation.
- Sampler defaults: 15 steps, cfg 1.0, `er_sde`, `simple`. Distilled Klein ignores
  negative prompts — keep the negative node empty, spend prompt space on positives.
- Custom nodes that matter: KJNodes (masks), **ComfyUI-Impact-Pack + Impact-Subpack**
  (FaceDetailer, UltralyticsDetectorProvider). Face model:
  `models/ultralytics/bbox/face_yolov8m.pt` (from `huggingface.co/Bingsu/adetailer`, per Subpack docs).
- ComfyUI-Manager must resolve as `venv-package` (pip `comfyui_manager` in the ComfyUI venv),
  not a legacy clone — otherwise MCP install/restart verbs refuse. See session notes 2026-11-03.
- `LoadImage` reads from `C:/DEV/ComfyUI/input/` by bare filename. Reference copies live there
  as `lineup_<slug>_ref.png`, byte-identical to `character-bible/approved_<slug>_reference.png`
  (verify with SHA256 when copying).

## The recipe (in order, every panel)

1. **Scene pass (all together).** One text-to-image run with ALL character refs wired into
   `ReferenceMultiLatent` (`images.image0..N`), bible prompt chunks, one master seed.
   Never generate characters separately and composite them — paste-ups always read as paste-ups
   (lighting/grain mismatch, repainted backdrops inside masks). Masked inserts regenerate everything
   inside the mask, including the backdrop — use them only for single-figure plates, never groups.
2. **Master seed.** One seed per issue for every panel (Session 1: `610933`). Failures re-roll
   at seed+1, +2. Same prompt + seed + graph = hash-identical pixels (deterministic, verified).
3. **FaceDetailer — runs AFTER the ref pass, at full 0.35.** `FaceDetailer` node, bbox model
   `bbox/face_yolov8m.pt`, denoise `0.35`, feather 5, guide 512/max 1024. Compares as faces-only:
   verify before/after pairs — if anything beyond faces moves, drop denoise to `0.2` (note: soft
   settings can re-crop framing; check composition after).
4. **Ref pass runs BEFORE the detailer: full 7-face one-pass, then FaceDetailer 0.35.** Batch40 ran
   all 4 order×strength combos × 5 seeds (20 images): 7-face-first won 4/5 boards outright (0.35 detailer after
   won 3 clear + 2 close-seconds; detailer-first won only 1). The masked `ReferenceMultiLatent` graph
   (`b39_faces_onepass.json` pattern: parallel branches off shared base pixels, per-face closeup ref +
   face-specific prompt at denoise `0.5`, lossless `ImageCompositeMasked` merges), THEN FaceDetailer 0.35 over
   the top. Face boxes: measure
   from the image (faceband strips), verify with a contact sheet BEFORE painting.
5. **Per-character eye wording where canon demands it.** The generic detail prompt washes out
   special eyes. Keechwah: "flat matte solid purple eyes, full-purple sclera, no white, no pupils,
   no glow, no shine, no light spill" (bible.md, 2026-11-03). If the detailer still leaves white,
   run a dedicated masked eye/face pass at denoise 0.4–0.6 with the character ref.
6. **Prop policing.** Gear tokens hijack generations: Gulgrim's shield rendered without him twice;
   Chip's staff grew axe heads and spear tips across four batches. When a prop crowds out its owner,
   strip gear tokens from the prompt first (person-only wording), reintroduce minimally.

## Prompt rules (Flux3 Klein specific)

- Identity chunks come from `character-bible/bible.md`, verbatim. Never invent faces.
- Height language moves the ladder but costs framing: explicit feet ("three-foot-tall halfling",
  "half the paladin's height") stages better; "high fantasy lineup" phrasing also helps but shrinks
  figures. Exact ratios (Shade = 1/2 Rocket, Gulgrim ≈ 2/3) do NOT come out of single-pass —
  enforce by measurement only (green-screen + key + scale), never by wording alone.
- Bills of particulars that work: `exactly two arms`, `both arms visible, both hands visible`,
  `boots flat on the floor/ground`, `adult faces, no children`.
- Max ~6 refs per ReferenceMultiLatent call (VRAM on 16 GB). Scene + 6 refs fits; watch VRAM.

## Batch discipline (lineup-lab)

- One batch dir per experiment: `character-bible/lineup-lab/batches/batch<N>/` with `img/`,
  the workflow JSONs, masks, and a `BATCHN-NOTES.md` (goal, runs table, verdict, pinned recipe).
- Generate DIRECTLY into `batches/batchN/img/`. Top-level `img/` holds keepers only.
- Name pairs so listings sort before→after: `<panel>a.png` (base), `<panel>b.png` (detail).
- Never commit during testing spikes — commit only on human go-ahead.
- Never touch another session's dirty files. The main checkout is shared: `git status` before
  every commit, stage ONLY your own paths (a bad `git add -A` once swept another session's work).

## Node-map gotchas (learned the hard way)

- Workflow JSON node numbers differ per family — always dump `class_type` per node id before
  patching, never assume. LoadImage-vs-VAELoader mixups cost whole batches.
- `LoadImageMask` requires `"channel": "red"`.
- `SetLatentNoiseMask` + denoise < 1.0 cannot form figures from clean pixels; inpainting needs
  denoise `1.0` with the noise mask.
- Unknown inputs to a node hard-fail (`SaveImage` got `images.image1` once) — validate by
  submitting, read `node_errors`.
- ComfyUI may serve STALE input images when a filename is overwritten — use fresh filenames
  per iteration, never rewrite in place.
- Pure-python PNG IO must implement all 5 filter types (None/Sub/Up/Average/Paeth); row slices
  are row-relative (`x * CH`), never flat-image offsets — both mistakes happened and both were silent.
- `pwsh` has no `for...do`, no `/dev/null`, no `sed`; pipe `echo "a b" | python submitb.py` for submits.

## Proven workflow files (copy, don't rebuild)

- 6-ref full scene: `sessions/session01/v2/s1p11.json` (plate-less text-to-image +
  `ReferenceMultiLatent` image0–5 on node 7, KSampler seed node 8, prefix node 10, master seed `610933`).
  Patch prompt + seed + prefix only; never touch wiring. Builder: root `scene_build.py`
  (base file + prompt txt + refs list + seed + prefix + out).
- FaceDetailer: `character-bible/lineup-lab/batches/batch21/lineuplab_b20_detail.json`
  (swap LoadImage, seed, SaveImage prefix only).
- Session panels: `sessions/session01/v2/*.json` + `sp_*.txt`/`sr_*.txt` prompt/ref sources.
- Submitter: root `submitb.py` (stdin `"<workflow> <out>"`), face/detail variants inline.
