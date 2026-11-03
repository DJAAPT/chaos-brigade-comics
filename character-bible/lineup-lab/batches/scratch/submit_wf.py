import json
import sys
import time
import urllib.request
from urllib.parse import quote

wf = sys.argv[1]
out = sys.argv[2]
g = json.load(open(wf))
base = "http://127.0.0.1:8188"
body = json.dumps({"prompt": g, "client_id": "lineup-submit"}).encode()
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
urllib.request.urlretrieve(dl, out)
print("downloaded", img["filename"])
