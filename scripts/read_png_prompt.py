"""Extract the executed prompt graph from ComfyUI's embedded PNG metadata."""
import glob
import json
import struct
import sys


def prompt_of(path):
    with open(path, "rb") as f:
        assert f.read(8) == b"\x89PNG\r\n\x1a\n"
        while True:
            hdr = f.read(8)
            if len(hdr) < 8:
                return None
            ln, typ = struct.unpack(">I4s", hdr)
            data = f.read(ln)
            f.read(4)
            if typ == b"tEXt" and data.startswith(b"prompt\x00"):
                return json.loads(data[7:].decode("latin-1"))
            if typ == b"IEND":
                return None


for pattern in sys.argv[1:]:
    for p in sorted(glob.glob(pattern)):
        g = prompt_of(p)
        print("===", p)
        if not g:
            print("  (no embedded prompt)")
            continue
        for nid, n in g.items():
            t = n.get("inputs", {}).get("text")
            if t:
                title = n["_meta"]["title"]
                print(f"  node {nid} [{title}] ({len(t)} chars):")
                print("   ", t[-300:])
        seeds = [
            (nid, k, v)
            for nid, n in g.items()
            for k, v in n.get("inputs", {}).items()
            if k in ("seed", "noise_seed")
        ]
        print("  seeds:", seeds)
