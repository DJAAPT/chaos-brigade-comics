import json
import time
import urllib.request
from urllib.parse import quote

g = json.load(open("workflows/lineuplab_b5b_duo.json"))
g["4"]["inputs"]["text"] = (
    "two adventurers posing on a neutral lineup wall with the concrete floor visible in front of them, "
    "on the left: young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair "
    "falling over the sides of his head, light stubble, no beard, warm brown eyes, subtle sly closed-mouth "
    "expression, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, belt dagger at hips, "
    "warm tan skin with a ruddy cast, long sideburns, small adult stature about three feet tall, exactly two arms, "
    "both arms relaxed away from his body and fully visible, both hands visible. "
    "on the right, stepping forward toward the viewer and larger in the foreground: adult male hill dwarf cleric, "
    "short stocky, completely bald head, broad long white beard, heavy furs, frost-covered boots, exactly two arms, "
    "both arms relaxed at his sides, both hands visible, both boots fully visible planted on the concrete floor in front "
    "of the wall. "
    "adult faces, no children, photorealistic, highly detailed"
)
g["13"]["inputs"]["seed"] = 424246
g["15"]["inputs"]["filename_prefix"] = "lineuplab_b5c_duo"
json.dump(g, open("workflows/lineuplab_b5c_duo.json", "w"), indent=2)

base = "http://127.0.0.1:8188"
body = json.dumps({"prompt": g, "client_id": "lineup-duo-c"}).encode()
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
urllib.request.urlretrieve(dl, "character-bible/lineup-lab/img/b5c_duo.png")
print("downloaded", img["filename"])
