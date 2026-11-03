import json

g = json.load(open("workflows/lineuplab_b19_heights.json"))
prompt = (
    "high fantasy police lineup: six adventurers standing side by side on a deep concrete floor in front of a plain "
    "neutral lineup wall, a single straight horizontal wall-floor joint behind them, one even concrete floor tone edge to edge, "
    "from left to right in rising height order: "
    "1) a three-foot-tall male halfling rogue, mid-20s, lean build, messy shaggy dark brown hair, "
    "light stubble, no beard, warm brown eyes, subtle sly closed-mouth expression, worn dark linen shirt with rolled sleeves, "
    "scuffed brown leather vest, warm tan skin with a ruddy cast, long sideburns, exactly two arms, both arms visible, "
    "both hands visible, boots flat on the floor. "
    "2) a four-foot-tall male hill dwarf cleric, short stocky, completely bald head, broad long white beard, heavy furs, "
    "frost-covered boots, warhammer at his side, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "3) an over-six-foot-tall male human paladin, short brown hair, light stubble, shining plate armor with gold phoenix crest "
    "on chest, red cape, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "4) a six-foot-two male wood elf ranger, long brown hair, green eyes, pointed ears, masculine jaw stubble, green cloak, "
    "longbow on back, exactly two arms, both arms visible, both hands visible, boots flat on the floor. "
    "5) a five-foot-eleven male human druid, brown skin, wild long white hair and white beard, brown eyes, "
    "green and brown fur garb, holding a straight wooden quarterstaff, exactly two arms, both arms visible, both hands visible, "
    "boots flat on the floor. "
    "6) a six-foot-tall male tiefling warlock, deep red skin, long curly black hair, goatee, large curved horns, "
    "glowing purple eyes, dark blue and gold robes, gold jewelry, exactly two arms, both arms visible, both hands visible, "
    "boots flat on the floor. "
    "adult faces, no children, photorealistic, highly detailed"
)
node = g.get("4")
inp = dict(node.get("inputs"))
inp.update({"text": prompt})
node.update({"inputs": inp})
ks = g.get("8")
ki = dict(ks.get("inputs"))
ki.update({"seed": 424260})
ks.update({"inputs": ki})
sv = g.get("10")
si = dict(sv.get("inputs"))
si.update({"filename_prefix": "lineuplab_b19_heights"})
sv.update({"inputs": si})
json.dump(g, open("workflows/lineuplab_b19_heights.json", "w"), indent=2)
print("patched")
