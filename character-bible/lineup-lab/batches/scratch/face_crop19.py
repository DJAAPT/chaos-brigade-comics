import measure_place as M

W, H, CH, im = M.read_png("character-bible/lineup-lab/img/b19_heights.png")
CX = (165, 445, 725, 895, 1050, 1180)
Y0, S = 60, 260
names = ("shade", "gulgrim", "rocket", "vadania", "chip", "keechwah")
for i, cx in enumerate(CX):
    x0 = max(0, min(W - S, cx - S // 2))
    crop = []
    for y in range(Y0, Y0 + S):
        row = bytearray()
        base = y * W
        for x in range(x0, x0 + S):
            o = (base + x) * CH
            row = row + im[y][o:o + CH]
        crop.append(row)
    M.write_png("C:/DEV/ComfyUI/input/f19_" + names[i] + ".png", S, S, CH, crop)
    print(names[i], x0, Y0)
print("done")
