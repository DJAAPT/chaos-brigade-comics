# Batch 34 — 11-person lineup, landscape canvas

Goal: retry batch33 portrait (832x1216, 8/11) in landscape so the row has room.

Fix: ReferenceMultiLatent's empty_latent = first ref latent x 0 — portrait refs force portrait canvas. Decoupled by adding EmptyLatentImage 1216x832 (same MP, transposed) as node 11 and rerouting KSampler latent_image from [7,2] to [11,0]. Conditioning still from all 11 refs. Seed 610934 (seed+1 per recipe).

Runs:
- b34_lineup11widea.png (base, 11 refs, 1216x832): 9/11 visible — Vadania, Chip, Rocketcandy, Keechwah (NEW, horns correct), Biggins, Thumba, Lilly, Gulgrim (NEW, front-row dwarf), Shade. Missing: Roland, Marigold. Faces/likenesses strong; Keechwah eyes red-glow not matte-purple (needs eye pass per pipeline §4 if keeper).
- b34_lineup11wideb.png (FaceDetailer 0.35, seed 610934): faces sharpened, composition unmoved.

Verdict: landscape + decoupled latent is the correct pattern for wide groups — add to pipeline. 11 still crowds out 2; two-shot split (or seed re-roll) for full 11. No commit (spike).
