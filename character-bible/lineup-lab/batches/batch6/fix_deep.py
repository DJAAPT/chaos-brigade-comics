import json
import struct
import time
import urllib.request
import zlib
from urllib.parse import quote

W, H = 1344, 768
SLOTS = [(300, 880, 30, 760), (820, 1264, 30, 760)]
raw = bytearray()
for y in range(H):
    raw.append(0)
    for x in range(W):
        v = 0
        for (x0, x1, y0, y1) in SLOTS:
            if x0 <= x < x1 and y0 <= y < y1:
                v = 255
                break
        raw.append(v)
rows = []
for y in range(H):
    lo = 1 + y * (W + 1)
    rows.append(bytearray(raw[lo:lo + W]))


def write_gray(p, w, h, rows):
    raw2 = bytearray()
    for r in rows:
        raw2.append(0)
        raw2 = raw2 + r

    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    open(p, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw2)))
        + chunk(b"IEND", b"")
    )


write_gray("C:/DEV/ComfyUI/input/lineup_mask_duo_deep2.png", W, H, rows)
print("mask written")

g = json.load(open("workflows/lineuplab_b5d_arms.json"))
for nid, node in g.items():
    if node.get("class_type") == "LoadImage":
        print(nid, node["inputs"].get("image"))
