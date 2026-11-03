import measure_place as M

W, H, CH, plate = M.read_png('C:/DEV/ComfyUI/input/lineup_wall_deep2.png')
FEET = 730
RH = 640
JOBS = [
    ('shade', 'character-bible/lineup-lab/img/b9b_green_shade.png', 3.0),
    ('gulgrim', 'character-bible/lineup-lab/img/b9c_green_gulgrim.png', 4.5),
    ('rocket', 'character-bible/lineup-lab/img/b9d_green_rocket.png', 6.2),
]

def keybox(im, w, h):
    top = h
    bot = -1
    l = w
    rr = -1
    for y in range(h):
        row = im[y]
        hit = False
        for x in range(w):
            o = x * CH
            if not (row[o + 1] > row[o] + 12 and row[o + 1] > row[o + 2] + 12):
                hit = True
                if x < l:
                    l = x
                if x > rr:
                    rr = x
        if hit:
            if y < top:
                top = y
            bot = y
    return top, bot, l, rr

def sample(im, w, h, fx, fy):
    x0 = int(fx)
    y0 = int(fy)
    ax = fx - x0
    ay = fy - y0
    x1 = x0 + 1 if x0 + 1 < w else x0
    y1 = y0 + 1 if y0 + 1 < h else y0
    r00 = im[y0]
    r10 = im[y1]
    out = []
    for c in range(CH):
        a00 = r00[x0 * CH + c]
        a10 = r00[x1 * CH + c]
        a01 = r10[x0 * CH + c]
        a11 = r10[x1 * CH + c]
        a0 = a00 + (a10 - a00) * ax
        a1 = a01 + (a11 - a01) * ax
        out.append(a0 + (a1 - a0) * ay)
    return out

figs = []
for job in JOBS:
    name = job[0]
    path = job[1]
    ft = job[2]
    _, _, _, im = M.read_png(path)
    w = len(im[0]) // CH
    h = len(im)
    top, bot, l, rr = keybox(im, w, h)
    s = (RH * ft / 6.2) / (bot - top + 1)
    figs.append((name, im, w, h, s, top, bot, l, rr))
    print(name, 'solo h=', bot - top + 1, 'scale=', round(s, 3))

canvas = [bytearray(r) for r in plate]
sizes = []
for f in figs:
    name, im, w, h, s, top, bot, l, rr = f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8]
    nh = max(1, int(round((bot - top + 1) * s)))
    nw = max(1, int(round((rr - l + 1) * s)))
    sizes.append((name, nw, nh))
    print(name, 'staged', nw, 'x', nh)

GAP = 40
total = sum(s[1] for s in sizes) + GAP * (len(sizes) - 1)
x = int((W - total) / 2)
for f, sz in zip(figs, sizes):
    name, im, w, h, s = f[0], f[1], f[2], f[3], f[4]
    top, bot, l, rr = f[5], f[6], f[7], f[8]
    nw, nh = sz[1], sz[2]
    y0 = FEET - nh + 1
    for yy in range(nh):
        dy = y0 + yy
        if dy < 0 or dy >= H:
            continue
        sy = top + yy / s
        for xx in range(nw):
            dx = x + xx
            if dx < 0 or dx >= W:
                continue
            sx = l + xx / s
            p = sample(im, w, h, sx, sy)
            if p[1] > p[0] + 12 and p[1] > p[2] + 30:
                continue
            a0 = p[0]
            a2 = p[2]
            g = p[1]
            if g > a0 and g > a2:
                g = a0 if a0 > a2 else a2
            dr = canvas[dy]
            o = dx * CH
            dr[o] = int(p[0])
            dr[o + 1] = int(g)
            dr[o + 2] = int(p[2])
    print(name, 'pasted at x=', x)
    x = x + nw + GAP
M.write_png('character-bible/lineup-lab/img/b12_trio_canon.png', W, H, CH, canvas)
print('wrote b12_trio_canon.png')
