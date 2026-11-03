import measure_place as M

W, H, CH, img = M.read_png("character-bible/lineup-lab/batches/batch32/img/b32_eyes2.png")
BOXES = ((1140, 1215, 180, 230), (1218, 1285, 175, 225))
out = [bytearray(r) for r in img]
n = 0
for (x0, x1, y0, y1) in BOXES:
    for y in range(y0, y1):
        for x in range(x0, x1):
            o = x * CH
            r0 = out[y][o]
            g0 = out[y][o + 1]
            b0 = out[y][o + 2]
            mx = r0
            if g0 > mx:
                mx = g0
            if b0 > mx:
                mx = b0
            mn = r0
            if g0 < mn:
                mn = g0
            if b0 < mn:
                mn = b0
            if mx > 90 and mx - mn < 45:
                k = (mx - 90) / 120
                if k > 1:
                    k = 1
                pr = 170 + (r0 - 90) * 0.3
                pg = 90 + (g0 - 90) * 0.3
                pb = 235
                out[y][o] = int(r0 + (pr - r0) * k)
                out[y][o + 1] = int(g0 + (pg - g0) * k)
                out[y][o + 2] = int(b0 + (pb - b0) * k)
                n = n + 1
print("recolored", n)
M.write_png("character-bible/lineup-lab/batches/batch32/img/b32_eyes_fixed.png", W, H, CH, out)
print("wrote fixed")
