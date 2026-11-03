import json
import struct
import time
import urllib.request
import zlib
from urllib.parse import quote

W, H = 1344, 768
SLOTS = [(380, 880, 40, 750), (820, 1264, 40, 750)]
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


write_gray("C:/DEV/ComfyUI/input/lineup_mask_duo.png", W, H, rows)
print("duo mask written")

shade = ("young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair "
       "falling over the sides of his head, light stubble, no beard, warm brown eyes, subtle sly closed-mouth "
       "expression, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, belt dagger at hips, "
       "warm tan skin with a ruddy cast, long sideburns, small adult stature about three feet tall, exactly two arms")
gul = ("adult male hill dwarf cleric, short stocky, completely bald head, broad long white beard, heavy furs, "
      "frost-covered boots, exactly two arms")
prompt = ("two adventurers standing side by side on a neutral lineup wall, on the left: " + shade
       + ". on the right, slightly taller: " + gul
       + ". adult faces, no children, photorealistic, highly detailed")
n1 = {"class_type": "LoadImage", "inputs": {"image": "lineup_wall_empty.png"}}
n2 = {"class_type": "LoadImageMask", "inputs": {"image": "lineup_mask_duo.png", "channel": "red"}}
n3 = {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_4b_int8_convrot.safetensors",
                                          "type": "flux3", "device": "default"}}
n4 = {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": prompt}}
n5 = {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": ""}}
n6 = {"class_type": "UNETLoader", "inputs": {"unet_name": "flux3-image-klein-nvfp4.safetensors",
                                          "weight_dtype": "default"}}
n7 = {"class_type": "VAELoader", "inputs": {"vae_name": "flux2-vae.safetensors"}}
n8 = {"class_type": "LoadImage", "inputs": {"image": "lineup_shade_ref.png"}}
n9 = {"class_type": "LoadImage", "inputs": {"image": "lineup_gulgrim_ref.png"}}
n10 = {"class_type": "ReferenceMultiLatent", "inputs": {"positive": ["4", 0], "resolution": "keep resolution",
         "negative": ["5", 0], "vae": ["7", 0], "images.image0": ["8", 0], "images.image1": ["9", 0]}}
n11 = {"class_type": "VAEEncode", "inputs": {"pixels": ["1", 0], "vae": ["7", 0]}}
n12 = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["11", 0], "mask": ["2", 0]}}
n13 = {"class_type": "KSampler", "inputs": {"model": ["6", 0], "seed": 424244, "steps": 15,
         "cfg": 1.0, "sampler_name": "er_sde", "scheduler": "simple",
         "positive": ["10", 0], "negative": ["10", 1], "latent_image": ["12", 0], "denoise": 1.0}}
n14 = {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["7", 0]}}
n15 = {"class_type": "SaveImage", "inputs": {"images": ["14", 0], "filename_prefix": "lineuplab_b5_duo"}}
g = {"1": n1, "2": n2, "3": n3, "4": n4, "5": n5, "6": n6, "7": n7,
     "8": n8, "9": n9, "10": n10, "11": n11, "12": n12, "13": n13, "14": n14, "15": n15}
json.dump(g, open("workflows/lineuplab_b5_duo.json", "w"), indent=2)

base = "http://127.0.0.1:8188"
body = json.dumps({"prompt": g, "client_id": "lineup-duo"}).encode()
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
urllib.request.urlretrieve(dl, "character-bible/lineup-lab/img/b5_duo.png")
print("downloaded", img["filename"])
