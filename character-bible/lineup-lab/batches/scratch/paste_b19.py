import measure_place as M

W, H, CH, canvas = M.read_png("character-bible/lineup-lab/img/b19_heights.png")
NAMES = ("shade", "gulgrim", "rocket", "vadania", "chip", "keechwah")
XS = (35, 315, 595, 765, 920, 1050)
Y0 = 60
S = 224
F = 8
jobs = list(zip(NAMES, XS))
for job in jobs:
    nm = job[0]
    x0 = job[1]
    _, _, _, crop = M.read_png("character-bible/lineup-lab/img/b18_face_" + nm + "2.png")
    print("paste", nm, x0)
    for yy in range(S):
        dy = Y0 + yy
        if dy < 0 or dy >= H:
            continue
        ex = yy + 1
        if S - yy < ex:
            ex = S - yy
        ey = ex
        fx = ex / F
        if fx > 1:
            fx = 1
        crow = crop[yy]
        drow = canvas[dy]
        for xx in range(S):
            dx = x0 + xx
            if dx < 0 or dx >= W:
                continue
            exx = xx + 1
            if S - xx < exx:
                exx = S - xx
            gx = exx if exx < ey else ey
            a = gx / F
            if a > 1:
                a = 1
            if a <= 0:
                continue
            o = dx * CH
            p = crow[xx * CH]
            q = crow[xx * CH + 1]
            r = crow[xx * CH + 2]
            b0 = drow[o]
            b1 = drow[o + 1]
            b2 = drow[o + 2]
            drow[o] = int(b0 + (p - b0) * a)
            drow[o + 1] = int(b1 + (q - b1) * a)
            drow[o + 2] = int(b2 + (r - b2) * a)
M.write_png("character-bible/lineup-lab/img/b19_final.png", W, H, CH, canvas)
print("wrote b19_final")
