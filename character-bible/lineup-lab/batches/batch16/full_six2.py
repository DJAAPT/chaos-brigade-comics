import json

g = json.load(open("workflows/lineuplab_b15_full_a.json"))

prompt = (
    "six adventurers standing side by side on a deep concrete floor in front of a plain neutral lineup wall, "
    "a single straight horizontal wall-floor joint behind them, one even concrete floor tone edge to edge, "
    "from left to right: "
    "1) young adult halfling man, mid-20s, messy shaggy dark brown hair, light stubble, worn dark linen shirt, "
    "scuffed brown leather vest, small adult stature about three feet tall, exactly two arms, both arms visible, "
    "both hands visible, boots flat on the floor. "
    "2) adult male hill dwarf cleric, short stocky, completely bald head, broad long white beard, heavy furs, "
    "frost-covered boots, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "3) adult male human paladin, short brown hair, light stubble, shining plate armor with gold phoenix crest on chest, "
    "red cape, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "4) adult male wood elf ranger, long brown hair, green eyes, pointed ears, masculine jaw stubble, green cloak, "
    "exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "5) adult male human druid, brown skin, wild long white hair and white beard, brown eyes, green and brown fur garb, "
    "exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "6) adult male tiefling warlock, deep red skin, long curly black hair, goatee, large curved horns, "
    "glowing purple eyes, dark blue and gold robes, exactly two arms, both arms visible, both hands visible, "
    "boots flat on the floor. "
    "adult faces, no children, photorealistic, highly detailed"
)
node4 = g.get("4")
inp4 = dict(node4.get("inputs"))
inp4.update({"text": prompt})
node4.update({"inputs": inp4})

g.update({"18": {"class_type": "LoadImage", "inputs": {"image": "lineup_vadania_ref.png"}}})
g.update({"19": {"class_type": "LoadImage", "inputs": {"image": "lineup_chip_ref.png"}}})
g.update({"20": {"class_type": "LoadImage", "inputs": {"image": "lineup_keechwah_ref.png"}}})
node10 = g.get("10")
inp10 = dict(node10.get("inputs"))
inp10.update({"images.image3": (18, 0)})
inp10.update({"images.image4": (19, 0)})
inp10.update({"images.image5": (20, 0)})
node10.update({"inputs": inp10})
node8 = g.get("8")
inp8 = dict(node8.get("inputs"))
inp8.update({"seed": 424256})
node8.update({"inputs": inp8})
node9 = g.get("9")
inp9 = dict(node9.get("inputs"))
inp9.update({"filename_prefix": "lineuplab_b16_full6_a"})
node9.update({"inputs": inp9})
json.dump(g, open("workflows/lineuplab_b16_full6_a.json", "w"), indent=2)
node8b = dict(node8.get("inputs"))
node8b.update({"seed": 424257})
node8.update({"inputs": node8b})
node9b = dict(node9.get("inputs"))
node9b.update({"filename_prefix": "lineuplab_b16_full6_b"})
node9.update({"inputs": node9b})
json.dump(g, open("workflows/lineuplab_b16_full6_b.json", "w"), indent=2)
print("ok ab")
