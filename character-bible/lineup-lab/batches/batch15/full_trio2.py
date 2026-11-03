import json

g = json.load(open("workflows/lineuplab_b9b_green_shade.json"))
g["4"]["inputs"]["text"] = (
    "three adventurers standing side by side on a deep concrete floor in front of a plain neutral lineup wall, "
    "a single straight horizontal wall-floor joint behind them, one even concrete floor tone edge to edge, "
    "on the left: young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair "
    "falling over the sides of his head, light stubble, no beard, warm brown eyes, subtle sly closed-mouth expression, "
    "worn dark linen shirt with rolled sleeves, scuffed brown leather vest, warm tan skin with a ruddy cast, long sideburns, "
    "small adult stature about three feet tall, half the height of the paladin, exactly two arms, "
    "both arms visible, both hands visible, boots flat on the floor. "
    "in the middle, a head taller than the halfling: adult male hill dwarf cleric, short stocky, completely bald head, "
    "broad long white beard, heavy furs, frost-covered boots, exactly two arms, both arms visible, both hands visible, "
    "boots flat on the floor. "
    "on the right, the tallest at over six feet, twice the halflings height: adult male human paladin, "
    "short brown hair, light stubble, shining plate armor with gold phoenix crest on chest, red cape, exactly two arms, "
    "both arms visible, both hands visible, boots flat on the floor. "
    "adult faces, no children, photorealistic, highly detailed"
)
g["6"]["inputs"]["image"] = "lineup_shade_ref.png"
g["16"] = {"class_type": "LoadImage", "inputs": {"image": "lineup_gulgrim_ref.png"}}
g["17"] = {"class_type": "LoadImage", "inputs": {"image": "lineup_rocketcandy_ref.png"}}
g["7"]["inputs"]["images.image0"] = ["6", 0]
g["7"]["inputs"]["images.image1"] = ["16", 0]
g["7"]["inputs"]["images.image2"] = ["17", 0]
g["8"]["inputs"]["seed"] = 424252
g["10"]["inputs"]["filename_prefix"] = "lineuplab_b15_full_a"
json.dump(g, open("workflows/lineuplab_b15_full_a.json", "w"), indent=2)
g["8"]["inputs"]["seed"] = 424253
g["10"]["inputs"]["filename_prefix"] = "lineuplab_b15_full_b"
json.dump(g, open("workflows/lineuplab_b15_full_b.json", "w"), indent=2)
print("ok a+b")
