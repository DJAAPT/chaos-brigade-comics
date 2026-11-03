import json
import sys
import time
import urllib.request
from urllib.parse import quote

g = json.load(open("workflows/lineuplab_b4h_floor.json"))
g["1"]["inputs"]["image"] = "lineup_b6e_comp.png"
g["2"]["inputs"]["image"] = "lineup_mask_flooronly.png"
g["4"]["inputs"]["text"] = (
    "even seamless concrete floor, uniform gray tone, same fine grain edge to edge, "
    "soft realistic contact shadows under boots, photorealistic, highly detailed"
)
g["10"]["inputs"]["seed"] = 424251
g["10"]["inputs"]["denoise"] = 0.45
g["12"]["inputs"]["filename_prefix"] = "lineuplab_b6h_flooronly"
json.dump(g, open("workflows/lineuplab_b6h_flooronly.json", "w"), indent=2)

base = "http://127.0.0.1:8188"
body = json.dumps({"prompt": g, "client_id": "lineup-flooronly"}).encode()
req = urllib.request.Request(base + "/prompt", data=body, headers={"Content-Type": "application/json"})
pid = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
print("queued", pid)
deadline = time.time() + 300
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
urllib.request.urlretrieve(dl, "character-bible/lineup-lab/img/b6h_flooronly.png")
print("downloaded", img["filename"])
