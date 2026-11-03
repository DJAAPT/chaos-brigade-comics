import measure_place as M

PW, PH, PCH, plate = M.read_png('C:/DEV/ComfyUI/input/lineup_wall_deep2.png')
JOINT = 633
FEET = 730
RH = 640

jobs = [
    ('shade', 'character-bible/lineup-lab/img/b9b_green_shade.png', 3.0),
    ('gul', 'character-bible/lineup-lab/img/b9c_green_gulgrim.png', 4.5),
    ('rocket', 'character-bible/lineup-lab/img/b9d_green_rocket.png', 6.2),
]


def key_mask(im, w, h, ch):
    m = bytearray(w * h)
    for y in range(h):
        row = im[y]
        base = y * w
        for x in range(w):
            o = x * ch
            g = row[o + 1]
            if not (g > row[o] + 25 and g > row[o + 2] + 25):
                m[base + x] = 1
    return m


def bbox(m, w, h):
    top = -1
    bot = -1
    l = w
    r = -1
    for y in range(h):
        hit = False
        base = y * w
        for x in range(w):
            if m[base + x]:
                hit = True
                if x < l:
                    l = x
                if x > r:
                    r = x
        if hit:
            if top <  0:
                top = y
            bot = y
    return top, bot, l, r


figs = []
for name, path, ft in jobs:
    w, h, ch, im = M.read_png(path)
    m = key_mask(im, w, h, ch)
    top, bot, l, r = bbox(m, w, h)
    th = RH * ft / 6.2
    s = th / (bot - top + 1)
    figs.append((name, im, w, h, ch, m, s, top, bot, l, r))
    print(name, 'solo h=', bot - top + 1, 'scale=', round(s, 3), 'target=', round(th))

def sample(img, w, h, ch, fx, fy):
    x0 = int(fx)
    y0 = int(fy)
    ax = fx - x0
    ay = fy - y0
    x1 = x0 + 1 if x0 + 1 < w else x0
    y1 = y0 + 1 if y0 + 1 < h else y0
    r00 = img[y0]
    r01 = img[y0]
    r10 = img[y1]
    r11 = img[y1]
    out = []
    for c in range(ch):
        a00 = r00[x0 * ch + c]
        a10 = r00[x1 * ch + c]
        a01 = r10[x0 * ch + c]
        a11 = r10[x1 * ch + c]
        a0 = a00 + (a10 - a00) * ax
        a1 = a01 + (a11 - a01) * ax
        out.append(a0 + (a1 - a0) * ay)
    return out


def scale_fig(im, w, h, ch, m, top, bot, l, r, s):
    sw = max(1, int(round((r - l + 1) * s)))
    sh = max(1, int(round((bot - top + 1) * s)))
    rgb = []
    alp = []
    for yy in range(sh):
        rrow = []
        arow = []
        sy = top + yy / s
        for xx in range(sw):
            sx = l + xx / s
            p = sample(im, w, h, ch, sx, sy)
            rrow.extend(p)
            x0 = int(sx)
            y0 = int(sy)
            ax = sx - x0
            ay = sy - y0
            x1 = x0 + 1 if x0 + 1 < w else x0
            y1 = y0 + 1 if y0 + 1 < h else y0
            m00 = m[y0 * w + x0]
            m10 = m[y0 * w + x1]
            m01 = m[y1 * w + x0]
            m11 = m[y1 * w + x1]
            m0 = m00 + (m10 - m00) * ax
            m1 = m01 + (m11 - m01) * ax
            arow.append(m0 + (m1 - m0) * ay)
        rgb.append(rrow)
        alp.append(arow)
    return sw, sh, rgb, alp


scaled = []
for name, im, w, h, ch, m, s, top, bot, l, r in figs:
    sw, sh, rgb, alp = scale_fig(im, w, h, ch, m, top, bot, l, r, s)
    scaled.append((name, sw, sh, rgb, alp))
    print(name, 'staged', sw, 'x', sh)

GAP = 40
total = sum(sw for _, sw, _, _, _ in scaled) + GAP * (len(scaled) - 1)
x = int((PW - total) / 2)
canvas = [bytearray(r) for r in plate]
for name, sw, sh, rgb, alp in scaled:
    ty = FEET - sh + 1
    for yy in range(sh):
        dy = ty + yy
        if dy < 0 or dy >= PH:
            continue
        for xx in range(sw):
            dx = x + xx
            if dx < 0 or dx >= PW:
                continue
            a = alp[yy][xx]
            if a <= 0:
                continue
            if a > 1:
                a = 1
            p = rgb[yy]
            po = xx * 3
            gg = p[po + 1]
            if gg > p[po] + 30 and gg > p[po + 2] + 30:
                continue
            dr = canvas[dy]
            o = dx * PCH
            p = rgb[yy]
            po = xx * 3
            for c in range(PCH):
                fg = p[po + c]
                if c == 1:
                    fg = min(fg, max(p[po], p[po + 2]) + 12)
                dr[o + c] = int(dr[o + c] * (1 - a) + fg * a)
    x += sw + GAP
    print(name, 'pasted')
M.write_png('character-bible/lineup-lab/img/b10_trio_staged.png', PW, PH, PCH, canvas)
print('wrote b10_trio_staged.png')
