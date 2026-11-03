import json

g = json.load(open("workflows/lineuplab_b14_unify.json"))
g["1"]["inputs"]["image"] = "lineup_b16_face_shade.png"
g["4"]["inputs"]["text"] = (
    "close-up face of a young adult halfling man, mid-20s, mature adult face, messy shaggy dark brown hair, "
    "light stubble, no beard, warm brown eyes looking at the viewer, subtle sly closed-mouth expression, "
    "warm tan skin with a ruddy cast, photorealistic, highly detailed"
)
g["6"]["inputs"]["image"] = "lineup_shade_ref.png"
g["8"]["inputs"]["seed"] = 424260
g["9"]["inputs"]["denoise"] = 0.35
g["12"]["inputs"]["filename_prefix"] = "lineuplab_b17_face_shade"
json.dump(g, open("workflows/lineuplab_b17_face_shade.json", "w"), indent=2)
print("ok")
