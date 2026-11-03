import measure_place as M

SEEDS = (424270, 424271, 424272, 424273, 424274, 424275, 424276, 424277, 424278, 424279)
TW, TH, COLS = 268, 154, 5
N = 0
for s in SEEDS:
    N = N + 1
ROWS = (N + COLS - 1) // COLS
W = TW * COLS
H = TH * ROWS
CH = 3
canvas = []
for y in range(H):
    canvas.append(bytearray(W * CH))
for idx, s in enumerate(SEEDS):
    _, _, _, im = M.read_png("character-bible/lineup-lab/img/b23_%d.png" % s)
    iw, ih = 1344, 768
    ox = (idx % COLS) * TW
    oy = (idx // COLS) * TH
    for yy in range(TH):
        sy = yy * ih // TH
        for xx in range(TW):
            sx = xx * iw // TW
            a = im[sy][sx * CH]
            b = im[sy][sx * CH + 1]
            c = im[sy][sx * CH + 2]
            o = (oy + yy) * W * CH + (ox + xx) * CH
            canvas[oy + yy][(ox + xx) * CH] = a
            canvas[oy + yy][(ox + xx) * CH + 1] = b
            canvas[oy + yy][(ox + xx) * CH + 2] = c
M.write_png("character-bible/lineup-lab/img/b23_contact.png", W, H, CH, canvas)
print("contact written", W, H)
