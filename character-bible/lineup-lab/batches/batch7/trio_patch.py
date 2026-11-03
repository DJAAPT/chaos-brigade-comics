import json

g = json.load(open("workflows/lineuplab_b5d_arms.json"))
g["1"]["inputs"]["image"] = "lineup_wall_deep.png"
g["2"]["inputs"]["image"] = "lineup_mask_trio.png"
g["4"]["inputs"]["text"] = (
    "three adventurers standing side by side on a deep concrete floor in front of a neutral lineup wall, "
    "on the left: young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair "
    "falling over the sides of his head, light stubble, no beard, warm brown eyes, subtle sly closed-mouth "
    "expression, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, "
    "warm tan skin with a ruddy cast, long sideburns, small adult stature about three feet tall, exactly two arms, "
    "both arms relaxed away from his body and fully visible, both hands open and visible at his sides. "
    "in the middle, a head taller: adult male hill dwarf cleric, short stocky, completely bald head, "
    "broad long white beard, heavy furs, frost-covered boots, exactly two arms, both arms relaxed at his sides, "
    "both hands visible, both boots fully visible planted on the concrete floor. "
    "on the right, the tallest: adult male human paladin, short brown hair, light stubble, "
    "shining plate armor with gold phoenix crest on chest, red cape, exactly two arms, "
    "both arms relaxed at his sides, both hands visible, both boots planted on the concrete floor. "
    "adult faces, no children, photorealistic, highly detailed"
)
g["16"] = {"class_type": "LoadImage", "inputs": {"image": "lineup_rocketcandy_ref.png"}}
g["10"]["inputs"]["images.image2"] = ["16", 0]
g["13"]["inputs"]["seed"] = 424253
g["15"]["inputs"]["filename_prefix"] = "lineuplab_b7_trio"
json.dump(g, open("workflows/lineuplab_b7_trio.json", "w"), indent=2)
print("trio workflow written")
