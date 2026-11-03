import measure_place as M

W, H, CH, img = M.read_png("character-bible/lineup-lab/batches/batch32/img/b32_eyes_fixed.png")
X0, X1, Y0, Y1 = 1080, 1135, 125, 165
out = [bytearray(r) for r in img]
n = 0
for y in range(Y0, Y1):
    for x in range(X0, X1):
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
        if mx > 70 and mx - mn < 45:
            out[y][o] = 150
            out[y][o + 1] = 70
            out[y][o + 2] = 220
            n = n + 1
print("painted", n)
M.write_png("character-bible/lineup-lab/batches/batch32/img/b32_eyes_fixed2.png", W, H, CH, out)
print("wrote fixed2")
