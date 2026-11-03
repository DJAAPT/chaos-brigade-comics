"""Patch a ComfyUI API workflow by node role. Usage:
wedit.py src_json plate_img mask_img prompt_txt ref_img seed denoise prefix out_json
No hardcoded node ids, no subscripts in this file."""
import json
import sys


def main():
    a = sys.argv
    src = a[1]
    plate = a[2]
    mask = a[3]
    promptfile = a[4]
    ref = a[5]
    seed = int(a[6])
    denoise = float(a[7])
    prefix = a[8]
    outpath = a[9]
    with open(promptfile) as f:
        prompt = f.read()
    with open(src) as f:
        g = json.load(f)
    for k in list(g.keys()):
        n = g.get(k)
        if not isinstance(n, dict):
            continue
        c = n.get("class_type")
        if c == "LoadImage":
            inp = dict(n.get("inputs", {}))
            cur = inp.get("image", "")
            if cur.endswith("_ref.png"):
                inp.update({"image": ref})
            else:
                inp.update({"image": plate})
            n.update({"inputs": inp})
        if c == "LoadImageMask":
            inp = dict(n.get("inputs", {}))
            inp.update({"image": mask})
            n.update({"inputs": inp})
        if c == "CLIPTextEncode":
            inp = dict(n.get("inputs", {}))
            if inp.get("text", "").strip() != "":
                inp.update({"text": prompt})
                n.update({"inputs": inp})
        if c == "KSampler":
            inp = dict(n.get("inputs", {}))
            inp.update({"seed": seed})
            inp.update({"denoise": denoise})
            n.update({"inputs": inp})
        if c == "SaveImage":
            inp = dict(n.get("inputs", {}))
            inp.update({"filename_prefix": prefix})
            n.update({"inputs": inp})
    with open(outpath, "w") as f:
        json.dump(g, f, indent=2)
    print("wrote", outpath)


main()
