import json
import struct
import sys
import time
import urllib.request
import zlib
from urllib.parse import quote


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png(p):
    d = open(p, "rb").read()
    pos = 8
    idat = b""
    w = 0
    h = 0
    ch = 3
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        t = d[pos + 4:pos + 8]
        if t == b"IDAT":
            idat = idat + d[pos + 8:pos + 8 + ln]
        if t == b"IHDR":
            w, h, bd, ct, cp, fm, im = struct.unpack(">IIBBBBB", d[pos + 8:pos + 8 + ln])
            ch = {0: 1, 2: 3, 6: 4}[ct]
        pos = pos + 12 + ln
    raw = zlib.decompress(idat)
    rows = []
    prev = bytearray(w * ch)
    i = 0
    stride = w * ch
    for _ in range(h):
        f = raw[i]
        i = i + 1
        line = bytearray(raw[i:i + stride])
        i = i + stride
        out = bytearray(stride)
        for k in range(stride):
            a = out[k - ch] if k >= ch else 0
            b = prev[k]
            c = prev[k - ch] if k >= ch else 0
            if f == 0:
                v = line[k]
            elif f == 1:
                v = (line[k] + a) & 255
            elif f == 2:
                v = (line[k] + b) & 255
            elif f == 3:
                v = (line[k] + ((a + b) >> 1)) & 255
            elif f == 4:
                v = (line[k] + paeth(a, b, c)) & 255
            else:
                raise ValueError(f)
            out[k] = v
        rows.append(out)
        prev = out
    return w, h, ch, rows


def write_png(p, w, h, ch, rows, gray=False):
    raw = bytearray()
    for r in rows:
        raw.append(0)
        raw = raw + r
    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    ct = 0 if gray else {1: 0, 3: 2, 4: 6}[ch]
    open(p, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw)))
        + chunk(b"IEND", b"")
    )


def bbox_vs_wall(fig_rows, wall_rows, w, h, ch, thresh=18):
    xs = []
    ys = []
    for y in range(h):
        fr = fig_rows[y]
        wr = wall_rows[y]
        for x in range(w):
            diff = 0
            for c in range(ch):
                diff = diff + abs(fr[x * ch + c] - wr[x * ch + c])
            if diff > thresh * ch:
                xs.append(x)
                ys.append(y)
                break
    if not xs:
        return None
    minx = min(xs)
    maxx = 0
    for y in range(h):
        fr = fig_rows[y]
        wr = wall_rows[y]
        for x in range(w - 1, -1, -1):
            diff = 0
            for c in range(ch):
                diff = diff + abs(fr[x * ch + c] - wr[x * ch + c])
            if diff > thresh * ch:
                if x > maxx:
                    maxx = x
                break
    return (minx, min(ys), maxx, max(ys))


WALL = "C:/DEV/ComfyUI/input/lineup_wall_empty.png"
PLATE = "C:/DEV/ComfyUI/input/lineup_plate_b2c.png"
GUL = "character-bible/lineup-lab/img/b4_gulgrim_solo.png"

if __name__ == "__main__":
    w, h, ch, wall = read_png(WALL)
    _, _, _, plate = read_png(PLATE)
    _, _, _, gul_rows = read_png(GUL)

    shade = (572, 52, 800, 756)
    gul = (460, 50, 904, 759)
    print("shade bbox (l,t,r,b):", shade)
    print("gulgrim solo bbox (l,t,r,b):", gul)

    gw = gul[2] - gul[0]
    gh = gul[3] - gul[1]
    print("gulgrim size:", gw, "x", gh)

    MARGIN = 30
    FEATHER = 24
    GAP = 20
    gx0 = shade[2] + GAP
    gx1 = gx0 + gw
    gy0 = gul[1]
    gy1 = gul[3]
    print("target paste x:", gx0, "to", gx1)
    if gx1 + MARGIN > w:
        print("WILL NOT FIT - need narrower staging")
        sys.exit(1)
    shift = gx0 - gul[0]
    print("shift:", shift)

    dst = []
    for y in range(h):
        line = bytearray(w * ch)
        src_row = gul_rows[y]
        if shift >= 0:
            line[shift * ch:] = src_row[:(w - shift) * ch]
            line[0:shift * ch] = wall[y][0:shift * ch]
        else:
            line[0:(w + shift) * ch] = src_row[(-shift) * ch:]
            line[(w + shift) * ch:] = wall[y][(w + shift) * ch:]
        dst.append(line)
    write_png("C:/DEV/ComfyUI/input/lineup_b4_measured.png", w, h, ch, dst)

    mx0 = max(0, gx0 - MARGIN)
    mx1 = min(w, gx1 + MARGIN)
    my0 = max(0, gy0 - MARGIN)
    my1 = min(h, gy1 + MARGIN)
    mrows = []
    for y in range(h):
        row = bytearray(w)
        for x in range(mx0, mx1):
            if y < my0 or y >= my1:
                continue
            dx = x - mx0
            ex = mx1 - 1 - x
            dy = y - my0
            ey = my1 - 1 - y
            m = dx
            if ex < m:
                m = ex
            if dy < m:
                m = dy
            if ey < m:
                m = ey
            row[x] = 255 if m >= FEATHER else int(255 * m / FEATHER)
        mrows.append(row)
    write_png("C:/DEV/ComfyUI/input/lineup_mask_gulgrim_m.png", w, h, 1, mrows, gray=True)
    print("mask rect:", mx0, my0, mx1, my1)

    n1 = {"class_type": "LoadImage", "inputs": {"image": "lineup_plate_b2c.png"}}
    n2 = {"class_type": "LoadImage", "inputs": {"image": "lineup_b4_measured.png"}}
    n3 = {"class_type": "LoadImageMask", "inputs": {"image": "lineup_mask_gulgrim_m.png", "channel": "red"}}
    n4 = {"class_type": "ImageCompositeMasked", "inputs": {
        "destination": ["1", 0],
        "source": ["2", 0],
        "x": 0,
        "y": 0,
        "resize_source": False,
        "mask": ["3", 0],
    }}
    n5 = {"class_type": "SaveImage", "inputs": {"images": ["4", 0], "filename_prefix": "lineuplab_b4e_measured"}}
    g = {"1": n1, "2": n2, "3": n3, "4": n4, "5": n5}
    json.dump(g, open("workflows/lineuplab_b4e_measured.json", "w"), indent=2)
    base = "http://127.0.0.1:8188"
    body = json.dumps({"prompt": g, "client_id": "lineup-4e"}).encode()
    req = urllib.request.Request(base + "/prompt", data=body, headers={"Content-Type": "application/json"})
    pid = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
    print("queued", pid)
    deadline = time.time() + 120
    hh = None
    while time.time() < deadline:
        try:
            hh = json.load(urllib.request.urlopen(base + "/history/" + pid, timeout=15))
        except Exception:
            hh = None
        if hh and pid in hh:
            break
        time.sleep(3)
    img = list(hh[pid]["outputs"].values())[0]["images"][0]
    dl = base + "/view?filename=" + quote(img["filename"]) + "&subfolder=&type=output"
    urllib.request.urlretrieve(dl, "character-bible/lineup-lab/img/b4e_measured.png")
    print("downloaded", img["filename"])
