import measure_place as M

W, H, CH, img = M.read_png("character-bible/lineup-lab/batches/batch16/img/b16_full6_keep.png")
print("keeper", W, H, CH)
CX = [112, 336, 560, 784, 1008, 1232]
Y0 = 80
S = 224
F = 12
for i, cx in enumerate(CX):
    x0 = min(max(0, cx - S // 2), W - S)
    y0 = Y0
    print(i, x0, y0)
    y0 = Y0
    crop = []
    for y in range(y0, y0 + S):
        row = bytearray()
        base = y * W
        for x in range(x0, x0 + S):
            o = x * CH
            Pix = img[y]
            row.extend(Pix[o:o + CH])
        crop.append(row)
    M.write_png("C:/DEV/ComfyUI/input/fc_%d.png" % i, S, S, CH, crop)
    mrows = []
    for y in range(S):
        mrow = bytearray(S)
        for x in range(S):
            dx = x + 1 if x < F else (S - x if x >= S - F else F)
            dy = y + 1 if y < F else (S - y if y >= S - F else F)
            m = dx if dx < dy else dy
            mrow[x] = 255 if m >= F else int(255 * m / F)
        mrows.append(mrow)
    M.write_png("C:/DEV/ComfyUI/input/fmask_%d.png" % i, S, S, 1, mrows, True)
print("crops+masks written")
