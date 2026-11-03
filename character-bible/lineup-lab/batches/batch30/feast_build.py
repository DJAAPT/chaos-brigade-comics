import json
import re

prompt = (
    "high fantasy inn feast at night, six adventurers eating and drinking together around a long wooden table "
    "in a warm torch-lit tavern, mugs of ale, platters of roast meat and bread, laughing and talking, "
    "camera facing the table so all six faces are visible, "
    "from left to right: "
    "1) a three-foot-tall male halfling rogue perched on a tall stool, messy shaggy dark brown hair, light stubble, "
    "worn dark linen shirt, scuffed brown leather vest, holding a mug, exactly two arms, both arms visible, both hands visible, "
    "photorealistic, highly detailed. "
    "2) a four-foot-tall male hill dwarf cleric seated on a bench, completely bald head, broad long white beard, "
    "heavy furs, a warhammer leaning against the bench, exactly two arms, both arms visible, both hands visible, "
    "photorealistic, highly detailed. "
    "3) an over-six-foot-tall male human paladin seated at the table, short brown hair, light stubble, "
    "shining plate armor with gold phoenix crest on chest, red cape draped over his chair, holding a mug, "
    "exactly two arms, both arms visible, both hands visible, photorealistic, highly detailed. "
    "4) a six-foot-two male wood elf ranger leaning on the table, long brown hair, green eyes, pointed ears, "
    "green cloak, longbow slung on back, exactly two arms, both arms visible, both hands visible, "
    "photorealistic, highly detailed. "
    "5) a five-foot-eleven male human druid seated with a straight plain wooden quarterstaff topped with a small slotted crystal "
    "leaning on his shoulder, no axe head, no blade, wild long white hair and white beard, green and brown fur garb, "
    "exactly two arms, both arms visible, both hands visible, photorealistic, highly detailed. "
    "6) a six-foot-tall male tiefling warlock seated at the table, deep red skin, long curly black hair, goatee, "
    "large curved horns, flat matte solid purple eyes with no sclera and no pupils, no glow, dark blue and gold robes, "
    "exactly two arms, both arms visible, both hands visible, photorealistic, highly detailed. "
    "adult faces, no children, photorealistic, highly detailed"
)
t = open("workflows/lineuplab_b22_try.json").read()
t = re.sub(r'"text": ".*?"', '"text": "' + prompt + '"', t, count=1)
t = t.replace("424261", "424300")
t = t.replace("lineuplab_b22_try", "lineuplab_b30_feast")
open("workflows/lineuplab_b30_feast.json", "w").write(t)
print("feast workflow written")
