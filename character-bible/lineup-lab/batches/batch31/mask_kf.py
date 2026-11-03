import measure_place as M

W, H = 1344, 768
X0, X1, Y0, Y1, F = 1020, 1320, 60, 320, 16
mrows = []
for y in range(H):
    row = bytearray(W)
    if Y0 <= y < Y1:
        fy = y - Y0 + 1
        if Y1 - y < fy:
            fy = Y1 - y
        for x in range(X0, X1):
            fx = x - X0 + 1
            if X1 - x < fx:
                fx = X1 - x
            f = fx if fx < fy else fy
            row[x] = 255 if f >= F else (f * 255) // F
    mrows.append(row)
M.write_png("C:/DEV/ComfyUI/input/fm_keech_feast.png", W, H, 1, mrows, True)
print("kee feast mask written")
