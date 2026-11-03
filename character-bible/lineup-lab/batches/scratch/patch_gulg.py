import json

g = json.load(open("workflows/lineuplab_b9b_green_shade.json"))
g["4"]["inputs"]["text"] = (
    "full-body studio photo of one single adult male hill dwarf cleric standing on a flat uniform green screen backdrop, "
    "short stocky, completely bald head, broad long white beard, heavy furs, frost-covered boots, "
    "exactly two arms, both arms relaxed at his sides, both hands visible, both boots flat on the ground, "
    "adult faces, no children, photorealistic, highly detailed"
)
g["6"]["inputs"]["image"] = "lineup_gulgrim_ref.png"
g["8"]["inputs"]["seed"] = 424262
g["10"]["inputs"]["filename_prefix"] = "lineuplab_b9c_green_gulgrim"
json.dump(g, open("workflows/lineuplab_b9c_green_gulgrim.json", "w"), indent=2)
print("ok")
