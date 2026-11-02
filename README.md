# Chaos Brigade Comics Pipeline
ComfyUI: http://10.13.37.88:8188 — this machine's LAN IP (http://127.0.0.1:8188 works too) (Flux3 Image Klein nvfp4, 5070 Ti)
Base workflow: workflows/base_flux3.json — Flux3 Image Klein text-to-image 1344x768, unet flux3-image-klein-nvfp4, CLIP qwen3vl_4b (type flux3), VAE flux2-vae, 15 steps / cfg 1.0 / er_sde / simple.

## Stages
1. **Character bible** — `character-bible/bible.md` (LOCKED, update only with approval)
2. **Scene director** — `scene-director/director.md` + `sessions/<id>/plan.json`
3. **Flux 3 generation** — `generate/` + `workflows/` (pinned JSON, seed log)
4. **Refinement** — re-roll bad limbs/duplicates, face detail pass (manual for v1)
5. **Comic production** — `comics/<id>.html` multipanel, narration + transcript quotes

## Quickstart (manual v1, what we did for S1)
```powershell
# 1. make workflow JSON from base + bible prompt (see scene-director/director.md)
# 2. submit:
C:\Users\St3v3D\AppData\Local\Python\pythoncore-3.14-64\Scripts\comfy.exe --json run --host 10.13.37.88 --port 8188 --workflow .\s1_p1.json
# 3. poll:
curl.exe -m 15 "http://10.13.37.88:8188/history/<prompt_id>"
# 4. download:
curl.exe -m 30 "http://10.13.37.88:8188/view?filename=<file>&subfolder=&type=output" -o .\s1_p1.png
```

## Auto (v2 target)
`scripts/new-session.ps1 -SessionId 69a905e...` → plan → generate → comic HTML.
See `scripts/new-session.ps1` skeleton.

## Conventions
- Session transcripts: `O:\ExternalSites\html\DND\session\<id>.json` (`.transcript`)
- Gallery refs: `O:\ExternalSites\html\DND\gallery\`
- Outputs: `sessions/<id>/panel_N.png` + `panels.json`
- Comics: `comics/<id>.html`, 1+ pages per session, 3-6 panels per page.
- Never commit Comfy API keys. Remote is LAN-only, no auth.
