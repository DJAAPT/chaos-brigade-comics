import measure_place as M

W, H, S, F = 1344, 768, 224, 12
BOXES = (35, 315, 595, 765, 920, 1050)
Y0 = 60
for i, x0 in enumerate(BOXES):
    mrows = []
    for y in range(H):
        mrow = bytearray(W)
        if Y0 <= y < Y0 + S:
            yy = y - Y0
            fy = yy + 1
            if S - yy < fy:
                fy = S - yy
            for x in range(x0, x0 + S):
                if x < 0 or x >= W:
                    continue
                xx = x - x0
                fx = xx + 1
                if S - xx < fx:
                    fx = S - xx
                f = fx if fx < fy else fy
                mrow[x] = 255 if f >= F else (f * 255) // F
        mrows.append(mrow)
    M.write_png("C:/DEV/ComfyUI/input/fm19_%d.png" % i, W, H, 1, mrows, True)
print("canvas masks written")
