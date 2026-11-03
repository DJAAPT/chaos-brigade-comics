import json

g = json.load(open("workflows/lineuplab_b7_trio.json"))
g["4"]["inputs"]["text"] = (
    "three adventurers standing side by side on a deep concrete floor in front of a plain neutral lineup wall, "
    "a single straight horizontal wall-floor joint behind them, one even concrete floor tone edge to edge, "
    "on the left: young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair "
    "falling over the sides of his head, light stubble, no beard, warm brown eyes, subtle sly closed-mouth expression, "
    "worn dark linen shirt with rolled sleeves, scuffed brown leather vest, warm tan skin with a ruddy cast, long sideburns, "
    "small adult stature about three feet tall, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "in the middle, a head taller: adult male hill dwarf cleric, short stocky, completely bald head, broad long white beard, "
    "heavy furs, frost-covered boots, warhammer at his side, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "on the right, the tallest at over six feet: adult male human paladin, short brown hair, light stubble, "
    "shining plate armor with gold phoenix crest on chest, red cape, exactly two arms, both arms visible, both hands visible, "
    "boots flat on the floor. "
    "adult faces, no children, photorealistic, highly detailed"
)
g["10"]["inputs"]["images.image2"] = ["16", 0]
del g["12"]
del g["2"]
g["13"]["inputs"]["latent_image"] = ["11", 0]
g["13"]["inputs"]["seed"] = 424252
g["15"]["inputs"]["filename_prefix"] = "lineuplab_b11_full_a"
json.dump(g, open("workflows/lineuplab_b11_full_a.json", "w"), indent=2)
g["13"]["inputs"]["seed"] = 424253
g["15"]["inputs"]["filename_prefix"] = "lineuplab_b11_full_b"
json.dump(g, open("workflows/lineuplab_b11_full_b.json", "w"), indent=2)
print("ok a+b")
