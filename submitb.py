import re
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import quote

lines = sys.stdin.read().split()
wf = lines[0]
out = lines[1]
base = "http://127.0.0.1:8188"
g = open(wf, "rb").read()
body = b'{"prompt": ' + g + b', "client_id": "dbg"}'
req = urllib.request.Request(base + "/prompt", data=body, headers={"Content-Type": "application/json"})
try:
    resp = urllib.request.urlopen(req, timeout=30).read()
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode()[:2000])
    raise SystemExit(1)
m = re.search(rb'"prompt_id":\s*"([^"]+)"', resp)
pid = m.group(1).decode()
print("queued", pid)
dl = None
for _ in range(100):
    time.sleep(3)
    try:
        h = urllib.request.urlopen(base + "/history/" + pid, timeout=15).read()
    except Exception:
        h = b""
    if b"outputs" in h:
        f = re.search(rb'"filename":\s*"([^"]+)"', h)
        if f:
            dl = base + "/view?filename=" + quote(f.group(1).decode()) + "&subfolder=&type=output"
            break
print("dl", dl)
urllib.request.urlretrieve(dl, out)
print("saved", out)
