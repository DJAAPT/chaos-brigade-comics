# Batch 33 — 11-person police lineup (all bible refs)

Goal: police lineup style shot of all 11 characters with approved refs in character-bible root, per PIPELINE.md single scene pass.

Refs (11, left-to-right = prompt order): vadania, chip, rocketcandy, keechwah, biggins, thumba, roland, gulgrim, lilly, marigold, shade.
Base: sessions/session01/v2/s1p11.json via scene_build.py. Seed 610933. Prefix b33_lineup11.

Runs:
- b33_lineup11a.png (base, 11 refs, seed 610933): queued ok on 16GB (5.9GB free) — no OOM. 8 faces visible: Vadania (far left, cropped), Chip, Rocketcandy, Biggins, Thumba (behind), Lilly, Roland, Shade. Missing: Keechwah, Gulgrim, Marigold (crowded out / occluded). Height ladder collapsed — back row reads same height, front row kneeling-scale. Prop policing held: Chip staff plain, no axe-head growth.
- b33_lineup11b.png (FaceDetailer, bbox/face_yolov8m.pt, denoise 0.35, seed 610933): faces sharpened, bodies/composition unmoved. Still 8/11.

Verdict: single-pass 11 exceeds ReferenceMultiLatent practical limit — confirms PIPELINE.md max ~6 refs and bible max-4 rule. For a true all-11 keeper: split into two group shots (party 6 + NPCs 5) on matching gray wall, or green-screen + scale per PROMPT-RULES. No commit (spike).
