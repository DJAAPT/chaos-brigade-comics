# Session 1 v3 — locked finish on v2 scenes/seeds

Same three scenes, same seed 610933, new finishing process (scene -> masked closeup ref passes -> FaceDetailer 0.35).
- v3_s1p11_3.png (p11 tavern): 6 faces refined; Gulgrim retro-converted bald->hairy canon in two extra passes (helmet at denoise 0.7, beard blackened with enlarged mask at 0.6). Lesson: 0.5 preserves layout (faces), structural canon changes need 0.6-0.7 + full-feature masks.
- v3_s1p32.png (p32 street): 5 hero faces refined; guards unmasked/untouched.
- v3_s1p43.png (p43 store): Chip + Roland refined; owlbear untouched.
- Compare vs v2b: sessions/session01/v2/img/s1p{11,32,43}b.png. User verdict: v3 better.
- Workflows: v3_<panel>_faces.json (N-branch one-pass) + v3_<panel>_detail.json.
