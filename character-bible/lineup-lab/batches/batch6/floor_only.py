"""Floor unify: repaint the whole floor band around (not over) the figures.

Figure mask = diff(b6e, deep plate) dilated; floor mask = rows below the
joint minus figure; low-denoise img2img for one even tone. Then the joint
line gets restored with restore_joint.py.
"""
import measure_place as M

W, H, CH, wall = M.read_png("C:/DEV/ComfyUI/input/lineup_wall_deep.png")
_, _, _, res = M.read_png("character-bible/lineup-lab/img/b6e_deep_duo.png")

TH = 60
fig = bytearray(W * H)
for y in range(H):
    rw = wall[y]
    rr = res[y]
    base = y * W
    for x in range(W):
        dd = 0
        for c in range(CH):
            dd += abs(rr[x * CH + c] - rw[x * CH + c])
        if dd > TH * CH:
            fig[base + x] = 1

R = 6
dil = bytearray(W * H)
for y in range(H):
    for x in range(W):
        if not fig[y * W + x]:
            continue
        for dy in range(-R, R + 1):
            yy = y + dy
            if 0 <= yy < H:
                lo = yy * W + max(0, x - R)
                hi = yy * W + min(W, x + R + 1)
                for p in range(lo, hi):
                    dil[p] = 1

JY, FTH = 548, 16
mrows = []
for y in range(H):
    row = bytearray(W)
    if y >= JY - FTH:
        ramp = y - (JY - FTH)
        a = 1.0 if ramp >= FTH else float(ramp) / FTH
        if a > 0:
            for x in range(W):
                if not dil[y * W + x]:
                    row[x] = int(255 * a)
    mrows.append(row)
M.write_png("C:/DEV/ComfyUI/input/lineup_mask_flooronly.png", W, H, 1, mrows, gray=True)
print("floor-only mask written")
