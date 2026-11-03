import measure_place as M

W, H = 1344, 768
BOXES = ((1150, 1200, 185, 225), (1225, 1275, 180, 220))
F = 8
mrows = []
for y in range(H):
    row = bytearray(W)
    for (x0, x1, y0, y1) in BOXES:
        if y0 <= y < y1:
            fy = y - y0 + 1
            if y1 - y < fy:
                fy = y1 - y
            for x in range(x0, x1):
                fx = x - x0 + 1
                if x1 - x < fx:
                    fx = x1 - x
                f = fx if fx < fy else fy
                v = 255 if f >= F else (f * 255) // F
                if v > row[x]:
                    row[x] = v
    mrows.append(row)
M.write_png("C:/DEV/ComfyUI/input/fm_keech_eyes_tight.png", W, H, 1, mrows, True)
print("tight eye mask written")
