import measure_place as M

W, H = 1344, 768
SLOTS = [(90, 430, 30, 760), (520, 880, 30, 760), (950, 1310, 30, 760)]

rows = []
for y in range(H):
    row = bytearray(W)
    for x in range(W):
        for (x0, x1, y0, y1) in SLOTS:
            if x0 <= x < x1 and y0 <= y < y1:
                row[x] = 255
    rows.append(row)
M.write_png("C:/DEV/ComfyUI/input/lineup_mask_trio.png", W, H, 1, rows, True)
print("trio mask written")
