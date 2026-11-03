import measure_place as M

W, H, CH, img = M.read_png("character-bible/lineup-lab/batches/batch32/img/b32_eyes_fixed2.png")
X0, Y0, S = 1060, 120, 280
crop = []
for y in range(Y0, Y0 + S):
    row = bytearray()
    src = img[y]
    base = X0 * CH
    row.extend(src[base:base + S * CH])
    crop.append(row)
M.write_png("character-bible/lineup-lab/batches/batch32/img/b32_kcrop3.png", S, S, CH, crop)
print("crop written")
