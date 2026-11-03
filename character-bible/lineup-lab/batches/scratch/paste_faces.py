import measure_place as M

W, H, CH, canvas = M.read_png("character-bible/lineup-lab/batches/batch16/img/b16_full6_keep.png")
NAMES = ("shade", "gulgrim", "rocket", "vadania", "chip", "keechwah")
XS = (0, 224, 448, 672, 896, 1120)
YS = (80, 80, 80, 80, 80, 80)
S = 224
for nm, x0, y0 in zip(NAMES, XS, YS):
    _, _, _, crop = M.read_png("character-bible/lineup-lab/img/b18_face_" + nm + ".png")
    i = 0
    for nn in NAMES:
        if nn == nm:
            break
        i = i + 1
    _, _, _, m = M.read_png("C:/DEV/ComfyUI/input/fmask_" + str(i) + ".png")
    FTH = 6
    for yy in range(S):
        dy = y0 + yy
        if dy < 0 or dy >= H:
            continue
        crow = crop[yy]
        mrow = m[yy]
        drow = canvas[dy]
        for xx in range(S):
            dx = x0 + xx
            if dx < 0 or dx >= W:
                continue
            a = mrow[xx]
            if a == 0:
                continue
            o = dx * CH
            p = crow[xx * CH]
            q = crow[xx * CH + 1]
            r = crow[xx * CH + 2]
            f = a / 255
            drow[o] = int(drow[o] * (1 - f) + p * f)
            drow[o + 1] = int(drow[o + 1] * (1 - f) + q * f)
            drow[o + 2] = int(drow[o + 2] * (1 - f) + r * f)
    print("pasted", nm)
M.write_png("character-bible/lineup-lab/img/b18_final.png", W, H, CH, canvas)
print("wrote b18_final")
