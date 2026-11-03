# Batch 3 — Gulgrim joins the plate (uncommitted)

Plate chain: `img/wall_empty.png` → b2c (Shade) → b4c composite (Shade + Gulgrim).

## Runs (seed 424243 throughout, same ref `lineup_gulgrim_ref.png` = hash `4be070c4` of approved ref)

| Run | Setup | Result |
|---|---|---|
| b3 | Full bible chunk incl. gear, into b2c plate, mask x830-1130 | FAIL — giant floating shield only, no dwarf |
| b3b | Person-first wording, same seed/plate/mask | FAIL — shield + hammer head, still no dwarf. Wording order is not the lever |
| b3c | Same as b3b but plate = empty wall (diagnostic) | INFO — dwarf body renders but shoved to mask left edge, clipped. Not a plate-occupancy problem: a scale/position problem |
| b3d | Wide mask x780-1180, b2c plate | PARTIAL — more gear (shield + hammer + fur), still no person. Gear tokens crowd the person out |
| b3e | Person-only prompt (no shield/warhammer tokens), wide mask, b2c plate | INFO — dwarf arm/leg/boot appear overlapping Shade: figure anchors left of slot, overflows. Placement is noise-driven, not mask-anchored |
| b3f | Mask moved right x860-1240, same prompt | FAIL — empty slot. Confirms placement drifts with noise; masks can't steer it |
| b4 | STOP tweaking. Solo-centered Gulgrim on empty wall, mask x420-920 (500px, Shade geometry) | PASS — full Gulgrim: bald, white beard, furs, rune shield, warhammer, frost boots. Matches approved ref |
| b4c | Deterministic composite: b2c plate + b4 shifted +300px, feathered mask (24px ramp), `ImageCompositeMasked`, no generation | PASS — Shade + Gulgrim side by side, both hold likeness, no bleed, seam nearly invisible |

## Pinned recipe (two-step group assembly)

1. Solo plate per character (batch-1/b2c recipe: masked denoise-1.0 insert on empty wall, centered 500px slot).
2. `ImageCompositeMasked` paste with feathered rect mask. Positions/scale fully deterministic — heights read exactly as staged.

## Rule learned

Second-person masked inserts into occupied plates are unreliable (placement drifts, gear crowds person). Solo-then-composite is the group path. Next: a taller character (Chip/Rocketcandy) to check height staging, then the same for all six.
