import json
import re

prompt = (
    "high fantasy street battle in Neverwinter at dusk, chaotic melee combat, six adventurers fighting corrupt city guards, "
    "guards in ornate helms with red plumes, red capes, gold phoenix crests, geometric diamond forearm tattoos, "
    "dynamic action poses, weapons mid-swing, dust and motion, lantern light and torch glow, "
    "the six heroes, left to right: "
    "1) a three-foot-tall male halfling rogue lunging with a dagger, messy shaggy dark brown hair, light stubble, "
    "worn dark linen shirt, scuffed brown leather vest, exactly two arms, photorealistic, highly detailed. "
    "2) a four-foot-tall male hill dwarf cleric swinging a warhammer, completely bald head, broad long white beard, "
    "heavy furs, large round shield with holy rune, exactly two arms, photorealistic, highly detailed. "
    "3) an over-six-foot-tall male human paladin raising a heavy battle-worn steel battleaxe, short brown hair, "
    "light stubble, shining plate armor with gold phoenix crest on chest, red cape flowing, exactly two arms, "
    "photorealistic, highly detailed. "
    "4) a six-foot-two male wood elf ranger drawing a longbow, long brown hair, pointed ears, green cloak, "
    "exactly two arms, photorealistic, highly detailed. "
    "5) a five-foot-eleven male human druid holding a straight plain wooden quarterstaff topped with a small slotted crystal, "
    "wild long white hair and white beard, green and brown fur garb, exactly two arms, photorealistic, highly detailed. "
    "6) a six-foot-tall male tiefling warlock casting purple eldritch energy from an orb, deep red skin, long curly black hair, "
    "goatee, large curved horns, glowing solid purple eyes with no sclera, dark blue and gold robes, exactly two arms, "
    "photorealistic, highly detailed. "
    "adult faces, no children, photorealistic, highly detailed"
)
jobs = (("workflows/lineuplab_b26_combat_a.json", 424290), ("workflows/lineuplab_b26_combat_b.json", 424291))
for path, seed in jobs:
    t = open(path).read()
    t = re.sub(r'"text": ".*?"', '"text": "' + prompt + '"', t, count=1)
    open(path, "w").write(t)
    g = json.load(open(path))
    g["8"]["inputs"]["seed"] = seed
    g["10"]["inputs"]["filename_prefix"] = "lineuplab_b26_combat_" + ("a" if seed == 424290 else "b")
    json.dump(g, open(path, "w"), indent=2)
    print("patched", path, seed)
