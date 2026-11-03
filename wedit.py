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
    f = open(promptfile)
    prompt = f.read()
    f.close()
    f = open(src)
    g = json.load(f)
    f.close()
    names = list(g.keys())
    done = 0
    for k in names:
        n = g.get(k)
        t = type(n)
        if str(t) != str(dict):
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
            tx = inp.get("text", "")
            s = tx.strip()
            if s != "" and done == 0:
                inp.update({"text": prompt})
                n.update({"inputs": inp})
                done = 1
        if c == "KSampler":
            inp = dict(n.get("inputs", {}))
            inp.update({"seed": seed})
            inp.update({"denoise": denoise})
            n.update({"inputs": inp})
        if c == "SaveImage":
            inp = dict(n.get("inputs", {}))
            inp.update({"filename_prefix": prefix})
            n.update({"inputs": inp})
    f = open(outpath, "w")
    json.dump(g, f, indent=2)
    f.close()
    print("wrote", outpath)


main()
