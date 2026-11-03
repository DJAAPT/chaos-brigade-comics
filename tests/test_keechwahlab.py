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
# Batch 22 ladder: 25-seed survey on the batch-21 block (master list seed
# 20261112, verified disjoint from all previously used seeds)
BATCH22_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 26)]
BATCH22_SEEDS = [904966445, 882449019, 1642844696, 1072951433, 497501377, 1045720643,
                 1869892708, 1520923251, 755491534, 2037017043, 891275891, 994132166,
                 2120284403, 1850888149, 1878731359, 108854776, 1307879905, 393500160,
                 1073082105, 511827512, 1465686071, 70683310, 468961277, 1405398255,
                 812935832]
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
# Batch 21: archetype noun instead of closure phrase — batch-19 verdict
# suggests "closed" invites a V-neck to close. "wizard robes" may carry
# closure implicitly (high collar, wrapped front) with no torso focus.
BATCH21_BLOCK = (
    "adult male tiefling warlock, warm bronze-tan skin with a faint red cast, "
    "long curly black hair, goatee, large curved bronze-brown horns rising upright "
    "side by side from the crown of his skull with bases buried deep in his thick "
    "curly hair, narrow almond-shaped human eyes under heavy eyelids, solid matte "
    "purple irises filling the entire visible eye with no visible sclera or pupil, "
    "male facial features, dark blue and gold wizard robes, gold jewelry, NO wings, "
    "sharply pointed canines, a thick tiefling tail behind him, exactly two arms"
)


class TestKeechwahLabDescriptions(unittest.TestCase):
    def load_block(self):
        self.assertTrue(os.path.exists(LAB_DESC), "keechwah-lab/descriptions.md missing (author it first)")
        blocks = parse_descriptions(LAB_DESC)
        self.assertEqual(set(blocks), {"keechwah"}, f"lab must hold exactly the keechwah block, got {set(blocks)}")
        return blocks["keechwah"]["text"], blocks["keechwah"]["sources"]

    def test_baseline_block_is_arm_b_verbatim(self):
        text, sources = self.load_block()
        self.assertEqual(text, BATCH21_BLOCK, "batch-21 block must carry wizard robes, no closure phrase")
        self.assertNotIn("worn closed", text)
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
        self.assertEqual(list(prompts), BATCH22_KEYS, "lab keys must be the batch-22 survey ladder in order")
        text, _ = TestKeechwahLabDescriptions().load_block()
        for i, key in enumerate(BATCH22_KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], BATCH22_SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {text}", f"{key} not exact composition")
            self.assertIn(entry["output"], (None, f"img/{key}.png"))
            self.assertEqual(list(entry["species_sources"].values()), [KEECHWAH_URL])

    def test_lab_workflows_family(self):
        import glob as _glob

        stems = [os.path.splitext(os.path.basename(p))[0] for p in _glob.glob("workflows/keechwahlab_*.json")]
        found = {s.removeprefix("keechwahlab_") for s in stems}
        self.assertEqual(found, set(BATCH22_KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts()
        for key in BATCH22_KEYS:
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
