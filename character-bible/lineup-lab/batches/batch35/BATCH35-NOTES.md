# Batch 35 — scale-fix attempt (same floor line + relative height)

Hypothesis (systematic debugging P3): Gulgrim rendered short in b34 because staging allowed a front-row crouch; explicit "same floor line, no kneeling, Gulgrim a full head taller than halfling, Shade shortest" would fix in single pass. Seed 610935, landscape 1216x832 decoupled latent (batch34 pattern).

Runs:
- b35_scalefixa.png: 10/11 — Vadania, Chip, Rocketcandy, Keechwah, Biggins, Thumba, Lilly, Gulgrim, Marigold (NEW), Shade. Missing: Roland. Faces strong.
- b35_scalefixb.png: FaceDetailer 0.35 — sharpened, composition unmoved.

Scale verdict: HYPOTHESIS FAILED. Gulgrim still renders shorter than Shade despite "full head taller" + same-line wording, even though front-row should read larger by perspective. Confirms PIPELINE.md: exact ratios do NOT come out of single-pass — enforce by measurement only (green-screen + key + scale), never by wording alone. Next for true scale: solo plates on matching wall + measure_place.py scale/paste, or accept stylized lineup.

Pattern: model caps at ~9-10 figures; Roland/Marigold trade off across seeds. No commit (spike).
