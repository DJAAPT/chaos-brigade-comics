# Batch 40 — 4 processes x 5 seeds (20 images + 5 boards)

Question: which finish wins across seeds — order (ref-pass vs detailer first) x strength (detailer 0.2 vs 0.35)?
- P1: 7-face on raw + detailer 0.2. P2: detailer 0.35 + 7-face. P3: 7-face on raw + detailer 0.35. P4: detailer 0.2 + 7-face.
- Seeds: 3596691034, 7169963536, 2150162665, 6470941741, 7505091016. Same scene prompt/refs, landscape decoupled latent.
- Face boxes re-measured per seed (faceband strips); seed 7505091016 rendered Lilly/Keechwah swapped — order lists adjusted per seed.
- Per-seed boards: compare_<seed>.png (rows P1/P2/P3/P4).
- User verdict: P3 wins 3/5 clear + 2 close-seconds (7505091016 went P1, 7169963536 went P2). Canonical finish: scene -> 7-face one-pass on raw -> FaceDetailer 0.35.
- All finals: b40_<seed>_{scene,d35,d2,fraw,p1,p2,p3,p4}.png. Masks: C:/DEV/ComfyUI/input/b40_<seed>_mask_<slug>.png.
