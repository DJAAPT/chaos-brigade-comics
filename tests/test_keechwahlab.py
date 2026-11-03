import json
import os
import unittest

from scripts.build_arm_b import ADDENDUM, PROMPT_KEYS, parse_descriptions
from tests.test_arm_c import FRAME_C, MODEL_PATH
from tests.test_build_sheet_bible import RACE_URL, SLUG_RACE

LAB_DIR = "character-bible/sheet-test/keechwah-lab"
LAB_DESC = os.path.join(LAB_DIR, "descriptions.md")
LAB_PROMPTS = os.path.join(LAB_DIR, "prompts.json")
KEYS = [f"keechwah_k{i:02d}" for i in range(1, 5)]
SEEDS = [424242, 424243, 777001, 424244]
# Batch 20 ladder: framing causality probe — batch-17 block (NO robe phrase)
# × the two cropped batch-19 seeds (r04=1602613270, r07=1826299574)
BATCH20_KEYS = ["keechwah_f01", "keechwah_f02"]
BATCH20_SEEDS = [1602613270, 1826299574]
# Batch 24 ladder: tail origin + tip + 10-seed check (master list seed
# 20261114, verified disjoint from all previously used seeds)
BATCH24_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 11)]
BATCH24_SEEDS = [275196493, 1034690049, 2080267707, 553890622, 2135411846, 105476702,
                 1879408468, 1015270008, 1846303153, 660577213]
# Batch 26 ladder: 25-seed survey on the batch-25 block (master list seed
# 20261115, verified disjoint from all previously used seeds)
BATCH26_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 26)]
BATCH26_SEEDS = [1292086694, 108847172, 2043092559, 693522991, 1510188667, 761833220,
                 1942551667, 826167318, 407826148, 198777561, 1029982029, 802084081,
                 644469806, 338508828, 2125720250, 682668388, 1445316900, 1461308820,
                 595204274, 1567244369, 1980263713, 1574338988, 754873136, 187601251,
                 1821554592]
# Batch 27 ladder: 10-seed check on the merged block (harvest script
# C:/Users/Andrew/AppData/Local/Temp/harvest27.py, master seed 20261116,
# verified disjoint from all 224 previously used seeds)
BATCH27_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 11)]
BATCH27_SEEDS = [903521648, 918981674, 1737432989, 1448841140, 1381742099, 56502011,
                 811032469, 28178984, 1563704135, 1052135545]
# Batch 28 ladder: 10-seed check on the tailless block (harvest script
# C:/Users/Andrew/AppData/Local/Temp/harvest27.py, master seed 20261117,
# verified disjoint from all 234 previously used seeds)
BATCH28_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 11)]
BATCH28_SEEDS = [625546482, 104806782, 1006179719, 868871769, 923435658, 1475067252,
                 1291660765, 929854378, 1480473186, 1997314573]
# Batch 3 ladder: 20-seed survey on the batch-2 block (master list seed
# 20261104, verified disjoint from all previously used seeds)
BATCH3_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 21)]
BATCH3_SEEDS = [897846952, 1387151110, 1592631768, 2142219592, 86866103, 979432203,
                1663594182, 27984743, 316266079, 1964552273, 1613333945, 121713292,
                1925297279, 688212631, 2023830113, 1027863760, 495423124, 1227329441,
                1250510708, 913730685]
KEECHWAH_URL = RACE_URL[SLUG_RACE["keechwah"]]
ARM_B_BLOCK = (
    "adult male tiefling warlock, deep red skin, long curly black hair, goatee, "
    "large curved horns, glowing purple eyes, male facial features, dark blue/gold robes, "
    "gold jewelry, NO wings, sharply pointed canines, a thick tiefling tail behind him, "
    "exactly two arms"
)
# Batch 25: user's full rewrite (sentence prose, no species word, smooth
# horns, hem-hidden spade tail) — tests the tiefling-drop + concealment
BATCH25_BLOCK = (
    "An adult male warlock with an athletic build and exactly two normal arms. "
    "He has warm bronze-tan human skin with a faint red cast, sharp masculine facial "
    "features, and sharply pointed canine teeth. His narrow, almond-shaped eyes rest "
    "under heavy eyelids, featuring solid matte purple irises that fill the entire "
    "visible eye with no white sclera or pupil. Long, thick, curly black hair frames "
    "his face alongside a neatly trimmed dark black goatee. Rising straight upright "
    "side by side from the crown of his skull are two smooth bronze-brown horns, their "
    "bases buried deep within his thick hair line. He wears elegant, flowing dark blue "
    "and gold wizard robes with ornate gold jewelry, and the spade tip of his thick "
    "bronze-tan tail peeks out from beneath the trailing hem of his robe on one side."
)
# Batch 27: merge — batch-25 prose + bible/ref horns (large curved ridged per
# user call; skin stays lab-locked bronze-tan per user call), glowing purple
# eyes (bible + ref glow, lab no-sclera structure), pointed ears + stern knowing
# expression + orb pendant (all from the approved ref), no-wings restored (NEVER)
BATCH27_BLOCK = (
    "An adult male warlock with an athletic build, exactly two normal arms, and no wings. "
    "He has warm bronze-tan human skin with a faint red cast, sharp masculine facial "
    "features with a stern, knowing expression, and sharply pointed canine teeth. His "
    "narrow, almond-shaped eyes rest under heavy eyelids, featuring solid glowing purple "
    "irises that fill the entire visible eye with no white sclera or pupil. Long, thick, "
    "curly black hair frames his face alongside a neatly trimmed dark black goatee, and "
    "his ears come to slight points. Rising from the crown of his skull are two large "
    "curved bronze-brown horns with a ridged texture, their bases buried deep within his "
    "thick hair line. He wears elegant, flowing dark blue and gold wizard robes with "
    "ornate gold jewelry including a purple orb pendant, and the spade tip of his thick "
    "bronze-tan tail peeks out from beneath the trailing hem of his robe on one side."
)
# Batch 28: tailless — batch-27 block verbatim minus the tail clause. The tail
# is the single most failure-prone element (hook-reads, escapes); the bible
# chunk carries no tail and no NEVER rule requires one.
BATCH28_BLOCK = (
    "An adult male warlock with an athletic build, exactly two normal arms, and no wings. "
    "He has warm bronze-tan human skin with a faint red cast, sharp masculine facial "
    "features with a stern, knowing expression, and sharply pointed canine teeth. His "
    "narrow, almond-shaped eyes rest under heavy eyelids, featuring solid glowing purple "
    "irises that fill the entire visible eye with no white sclera or pupil. Long, thick, "
    "curly black hair frames his face alongside a neatly trimmed dark black goatee, and "
    "his ears come to slight points. Rising from the crown of his skull are two large "
    "curved bronze-brown horns with a ridged texture, their bases buried deep within his "
    "thick hair line. He wears elegant, flowing dark blue and gold wizard robes with "
    "ornate gold jewelry including a purple orb pendant."
)


class TestKeechwahLabDescriptions(unittest.TestCase):
    def load_block(self):
        self.assertTrue(os.path.exists(LAB_DESC), "keechwah-lab/descriptions.md missing (author it first)")
        blocks = parse_descriptions(LAB_DESC)
        self.assertEqual(set(blocks), {"keechwah"}, f"lab must hold exactly the keechwah block, got {set(blocks)}")
        return blocks["keechwah"]["text"], blocks["keechwah"]["sources"]

    def test_baseline_block_is_arm_b_verbatim(self):
        text, sources = self.load_block()
        self.assertEqual(text, BATCH28_BLOCK, "batch-28 block must be the tailless merge verbatim")
        self.assertNotIn("tail", text)
        self.assertIn("no wings", text)
        self.assertIn("character-bible/Sheets/Keechwah.pdf", sources)
        self.assertIn(KEECHWAH_URL, sources)
        self.assertTrue(any("bible.md locked chunks" in s for s in sources))


class TestKeechwahLabPrompts(unittest.TestCase):
    def load_prompts(self):
        self.assertTrue(os.path.exists(LAB_PROMPTS), "keechwah-lab/prompts.json missing (run build_lab first)")
        with open(LAB_PROMPTS, encoding="utf-8") as f:
            return json.load(f)

    def test_lab_prompts_schema(self):
        prompts = self.load_prompts()
        self.assertEqual(list(prompts), BATCH28_KEYS, "lab keys must be the batch-28 ladder in order")
        text, _ = TestKeechwahLabDescriptions().load_block()
        for i, key in enumerate(BATCH28_KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], BATCH28_SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {text}", f"{key} not exact composition")
            self.assertIn(entry["output"], (None, f"img/{key}.png"))
            self.assertEqual(list(entry["species_sources"].values()), [KEECHWAH_URL])

    def test_lab_workflows_family(self):
        import glob as _glob

        stems = [os.path.splitext(os.path.basename(p))[0] for p in _glob.glob("workflows/keechwahlab_*.json")]
        found = {s.removeprefix("keechwahlab_") for s in stems}
        self.assertEqual(found, set(BATCH28_KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts()
        for key in BATCH28_KEYS:
            with open(f"workflows/keechwahlab_{key}.json", encoding="utf-8") as f:
                g = json.load(f)
            seeds = [n["inputs"][k] for n in g.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})]
            self.assertEqual(set(seeds), {prompts[key]["seed"]}, f"keechwahlab_{key} graph seed mismatch")
            saves = [n for n in g.values() if n["class_type"] == "SaveImage"]
            self.assertEqual(saves[0]["inputs"]["filename_prefix"], f"keechwahlab_{key}")

    def test_builder_slug_override(self):
        # pins the build_lab generalization: a non-shade slug builds cleanly
        import subprocess
        import sys
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/build_lab.py",
                 "--descriptions", LAB_DESC,
                 "--out-dir", tmp,
                 "--model-path", MODEL_PATH,
                 "--slug", "keechwah",
                 "--seeds", "424242",
                 "--keys", "keechwah_k01"],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(os.path.join(tmp, "prompts.json"), encoding="utf-8") as f:
                produced = json.load(f)
        self.assertEqual(list(produced), ["keechwah_k01"])
        self.assertEqual(produced["keechwah_k01"]["seed"], 424242)


if __name__ == "__main__":
    unittest.main()
