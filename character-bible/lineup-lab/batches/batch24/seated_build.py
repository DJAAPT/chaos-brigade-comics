import json
import re
import sys

seed = sys.argv[1]
prefix = sys.argv[2]
out = sys.argv[3]
prompt = (
    "high fantasy tavern theater interior at night, a lit wooden stage with a hooded minstrel performing under warm lantern light, "
    "six adventurers seated at round wooden tables with their backs to the viewer, watching the stage, mugs and candles on the tables, "
    "from left to right: "
    "1) a three-foot-tall male halfling rogue seen from behind, messy shaggy dark brown hair, worn dark linen shirt, "
    "scuffed brown leather vest, exactly two arms, photorealistic, highly detailed. "
    "2) a four-foot-tall male hill dwarf cleric seen from behind, completely bald head, heavy fur cloak, exactly two arms, "
    "photorealistic, highly detailed. "
    "3) an over-six-foot-tall male human paladin seen from behind, short brown hair, shining plate armor with gold phoenix crest, "
    "red cape draped over his chair, exactly two arms, photorealistic, highly detailed. "
    "4) a six-foot-two male wood elf ranger seen from behind, long brown hair, pointed ears, green cloak, longbow slung on back, "
    "exactly two arms, photorealistic, highly detailed. "
    "5) a five-foot-eleven male human druid seen from behind, wild long white hair, green and brown fur garb, "
    "holding a straight plain wooden quarterstaff, exactly two arms, photorealistic, highly detailed. "
    "6) a six-foot-tall male tiefling warlock seen from behind, deep red skin, long curly black hair, large curved horns, "
    "dark blue and gold robes, exactly two arms, photorealistic, highly detailed. "
    "adult figures, no children, photorealistic, highly detailed"
)
t = open("workflows/lineuplab_b22_try.json").read()
t = re.sub(r'"text": ".*?"', '"text": "' + prompt + '"', t, count=1)
t = t.replace("424261", seed)
t = t.replace("lineuplab_b22_try", prefix)
open(out, "w").write(t)
print("wrote", out)
