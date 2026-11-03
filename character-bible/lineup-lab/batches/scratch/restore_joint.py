"""Restore the wall/floor joint line from the plate behind the figures.

Figure mask = diff(result, plate) dilated; joint band rows copied from plate
wherever the pixels read as repainted wall (bright), with alpha feathered at the
restore-zone borders so no hard edge remains. Deterministic, no generation.
"""
import measure_place as M

W, H, CH, wall = M.read_png("C:/DEV/ComfyUI/input/lineup_wall_deep.png")
_, _, _, res = M.read_png("character-bible/lineup-lab/img/b6h_flooronly.png")

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

R = 3
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

Y0, Y1, FTH = 540, 585, 12
lo, hi = max(0, Y0 - FTH), min(H, Y1 + FTH)
ok = []
for y in range(lo, hi):
    rr = res[y]
    row = bytearray(W)
    for x in range(W):
        m = (rr[x * CH] + rr[x * CH + 1] + rr[x * CH + 2]) / 3
        if not dil[y * W + x] or m > 165:
            row[x] = 1
    ok.append(row)

out = [bytearray(r) for r in res]
n = 0
for i, y in enumerate(range(lo, hi)):
    rr = out[y]
    wr = wall[y]
    row = ok[i]
    ey = min(y - lo, hi - 1 - y)
    ay = 1.0 if ey >= FTH else float(ey) / FTH
    for x in range(W):
        if not row[x]:
            continue
        run = 0
        xx = x
        while xx >= 0 and row[xx]:
            run += 1
            xx -= 1
            if run > FTH:
                break
        run2 = 0
        xx = x
        while xx < W and row[xx]:
            run2 += 1
            xx += 1
            if run2 > FTH:
                break
        ex = run if run < run2 else run2
        ax = 1.0 if ex > FTH else float(ex) / FTH
        a = ax if ax < ay else ay
        if a <= 0:
            continue
        for c in range(CH):
            a0 = rr[x * CH + c]
            b0 = wr[x * CH + c]
            rr[x * CH + c] = int(a0 + (b0 - a0) * a)
        n += 1
print("blended pixels:", n)
M.write_png("character-bible/lineup-lab/img/b6i_joint.png", W, H, CH, out)
print("wrote b6i_joint.png")
