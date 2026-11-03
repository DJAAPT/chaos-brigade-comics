import copy
import json
import time
import urllib.request
from urllib.parse import quote

BASE = "http://127.0.0.1:8188"
SEEDS = (424295, 424296, 424297, 424298, 424299)


def run_graph(g, tag):
    body = json.dumps({"prompt": g, "client_id": tag}).encode()
    req = urllib.request.Request(BASE + "/prompt", data=body, headers={"Content-Type": "application/json"})
    pid = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
    print(tag, "queued", pid)
    deadline = time.time() + 600
    hh = None
    while time.time() < deadline:
        try:
            hh = json.load(urllib.request.urlopen(BASE + "/history/" + pid, timeout=15))
        except Exception:
            hh = None
        if hh and pid in hh:
            break
        time.sleep(5)
    outs = list(hh[pid]["outputs"].values())
    return outs[0]["images"][0]


def fetch(img, out):
    q = "filename=" + quote(img["filename"]) + "&subfolder=&type=output"
    urllib.request.urlretrieve(BASE + "/view?" + q, out)
    print("saved", out)


lineup = json.load(open("workflows/lineuplab_b22_try.json"))
detail = json.load(open("character-bible/lineup-lab/batches/batch21/lineuplab_b20_detail.json"))
for s in SEEDS:
    g = json.loads(json.dumps(lineup))
    g["8"]["inputs"]["seed"] = s
    g["10"]["inputs"]["filename_prefix"] = "lineuplab_b29_%d" % s
    img = run_graph(g, "lineup-%d" % s)
    fetch(img, "C:/DEV/ComfyUI/input/lineup_b29_%d.png" % s)
    fetch(img, "character-bible/lineup-lab/batches/batch29/img/b29_%d_before.png" % s)
    d = json.loads(json.dumps(detail))
    d["6"]["inputs"]["image"] = "lineup_b29_%d.png" % s
    d["8"]["inputs"]["seed"] = s + 1000
    d["9"]["inputs"]["filename_prefix"] = "lineuplab_b29d_%d" % s
    img2 = run_graph(d, "detail-%d" % s)
    fetch(img2, "character-bible/lineup-lab/batches/batch29/img/b29_%d_after.png" % s)
print("batch done")
