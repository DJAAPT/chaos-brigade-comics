# FLUX 3 Image Klein — manual download checklist

Status: COMPLETE (2026-11-01). Model files installed; the comics pipeline
now runs Flux3-only (see README) — Flux2 is no longer used for generation.
`flux3` CLIP type and `ReferenceMultiLatent` are confirmed live on `127.0.0.1:8188`.

Source in use: **Civitai** (account required to download). Every file there is
byte-identical to BFL's official ComfyUI release — all SHA256s verified
against `black-forest-labs/flux-3-image-klein-comfy`, uploaded by the
`CivitaiOfficial` account, virus + pickle scan clean.

Other verified-identical sources, if Civitai is ever down:
`https://huggingface.co/ml-resources/flux-3-image-klein-comfy/resolve/main/`
(ungated mirror), or the gated official repo after accepting the license.

## Civitai filename mapping

Civitai serves opaque names like `flux3Klein_klein_3299296.safetensors`.
Rename on save — or the official templates won't match their dropdowns.

| Civitai file | Size | Save as |
|---|---|---|
| Klein → nvfp4 diffusion | 4.92 GB | `flux3-image-klein-nvfp4.safetensors` |
| Klein → int8 text encoder | **4.52 GB** | `qwen3vl_4b_int8_convrot.safetensors` |
| Klein → int8 upsampler | 9.08 GB | `qwen3.5_9b_flux3_prompt_upsampler_int8_convrot.safetensors` |
| Klein-Base → nvfp4 diffusion | 4.90 GB | `flux3-image-klein-base-nvfp4.safetensors` |

Two of the three text encoders on Civitai are int8 — take the **4.52 GB**
one. The 9.08 GB int8 is the upsampler, the 8.27 GB is bf16.

## VAE — already correct, do NOT download

Your `C:\DEV\ComfyUI\models\vae\flux2-vae.safetensors` hashes to
`d64f3a68e1cc4f9f4e29b6e0da38a0204fe9a49f2d4053f0ec1fa1ca02f9c4b5`,
matching Comfy-Org's official Flux2 VAE exactly. Flux3 reuses this VAE.
(BFL's own copy has a different hash — Comfy-Org repackaged it. Yours is the
right one for ComfyUI.)

## Which build? NVFP4, not int8

Your 5070 Ti is Blackwell, which has **native FP4 tensor cores**. NVFP4 is
both smaller and faster than int8-convrot on this card. Use it.

(The official templates ship int8-convrot because they target a wide range of
GPUs. For a 5070 Ti specifically, NVFP4 is the better build. int8 stays
available as the fallback — see `-Quant int8` below.)

## Required (minimum test: ~9.4 GB)

| File | Size | Destination |
|---|---|---|
| `flux3-image-klein-nvfp4.safetensors` | 4.92 GB | `C:\DEV\ComfyUI\models\diffusion_models\` |
| `qwen3vl_4b_int8_convrot.safetensors` | 4.52 GB | `C:\DEV\ComfyUI\models\text_encoders\` |

The first is the step-distilled generator (15 steps, the fast one).
The second is the text encoder — **not optional**, Flux3 needs Qwen3-VL-4B.
There is no NVFP4 text encoder, so int8 is the smallest available.
You already have the VAE it wants (`flux2-vae.safetensors`).

## Recommended (+11.2 GB)

| File | Size | Destination |
|---|---|---|
| `flux3-image-klein-base-nvfp4.safetensors` | 4.90 GB | `C:\DEV\ComfyUI\models\diffusion_models\` |
| `qwen3.5_9b_flux3_prompt_upsampler_w4a8.safetensors` | 6.26 GB | `C:\DEV\ComfyUI\models\text_encoders\` |

Base = undistilled, 50 steps, the quality reference for a fair comparison
against your Flux2-Dev 32B. Official multi-reference edit template uses this one.

Upsampler = expands short prompts into rich captions. Your bible prompts are
already detailed, so this is a nice-to-have, not a blocker.

## Not needed

- **`black-forest-labs/flux-3-image-klein` `model.safetensors`** — wrong repo.
  That's the diffusers-layout release (11.1 GB bf16 monolith). ComfyUI needs
  the split files from the `-comfy` repo.
- **`jonathan-golden/flux3-klein-nvfp4`** — third-party diffusers-layout
  re-upload (sharded text encoder, `variants/nvfp4/` dir). Not ComfyUI format,
  not from BFL, not verified. Skip it.
- bf16 builds (11 GB each) — 24 GB+ VRAM cards only. You have 16.
- Any LoRA — Flux3 LoRAs barely exist yet; your Flux1/Flux2 LoRAs won't work.

## Run it yourself (optional)

`generate/download-flux3.ps1` downloads the full set with SHA256
verification. NVFP4 by default:

```powershell
powershell -ExecutionPolicy Bypass -File "O:\Scripts\chaos-brigade-comics\generate\download-flux3.ps1"
```

Add `-Minimal` to skip the base model and upsampler (~9.4 GB instead of ~20 GB),
or `-Quant int8` to fall back to the int8-convrot builds.

## After the files land

1. Restart ComfyUI (the batch file on your Desktop) so it rescans models.
2. Tell me and I'll build the multi-reference flow, wire in the approved
   party portraits, and generate a side-by-side against
   `sessions/session01/panel1_tavern.png`.

Flux2's setup is retired from the pipeline; files on disk remain but nothing uses them.
