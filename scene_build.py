import json
import sys

base = sys.argv[1]
promptfile = sys.argv[2]
refsfile = sys.argv[3]
seed = int(sys.argv[4])
prefix = sys.argv[5]
out = sys.argv[6]
with open(promptfile) as f:
    prompt = f.read()
refs = open(refsfile).read().split()
g = json.load(open(base))
g["4"]["inputs"]["text"] = prompt
for i in range(6):
    key = "images.image%d" % i
    if key in g["7"]["inputs"]:
        del g["7"]["inputs"][key]
for i, r in enumerate(refs):
    nid = str(20 + i)
    g[nid] = {"class_type": "LoadImage", "inputs": {"image": r}}
    g["7"]["inputs"]["images.image%d" % i] = [nid, 0]
g["8"]["inputs"]["seed"] = seed
g["10"]["inputs"]["filename_prefix"] = prefix
json.dump(g, open(out, "w"), indent=2)
print("wrote", out, len(refs), "refs")
