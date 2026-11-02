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
# Batch 6 ladder: 20-seed survey on the batch-5 block (master list seed
# 20261105, verified disjoint from all previously used seeds)
BATCH6_KEYS = [f"keechwah_r{i:02d}" for i in range(1, 21)]
BATCH6_SEEDS = [552830877, 648655267, 422035164, 1761674982, 729454402, 1819679304,
                1275567273, 731620070, 1959001081, 1342234658, 792120332, 730621735,
                114543239, 1319299462, 1152315787, 1449114899, 206960085, 2084635009,
                290107592, 2051182405]
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
# Batch 5: horns grown, not stuck on — batch 4 skin holds everywhere but
# k03's leftover red, which reads seed-specific rather than wording
BATCH5_BLOCK = (
    "adult male tiefling warlock, warm bronze-tan skin with a faint red cast, "
    "long curly black hair, goatee, large curved horns growing naturally from his "
    "temples and emerging through his hair, glowing purple eyes, male facial features, "
    "dark blue/gold robes, gold jewelry, NO wings, sharply pointed canines, "
    "a thick tiefling tail behind him, exactly two arms"
)


class TestKeechwahLabDescriptions(unittest.TestCase):
    def load_block(self):
        self.assertTrue(os.path.exists(LAB_DESC), "keechwah-lab/descriptions.md missing (author it first)")
        blocks = parse_descriptions(LAB_DESC)
        self.assertEqual(set(blocks), {"keechwah"}, f"lab must hold exactly the keechwah block, got {set(blocks)}")
        return blocks["keechwah"]["text"], blocks["keechwah"]["sources"]

    def test_baseline_block_is_arm_b_verbatim(self):
        text, sources = self.load_block()
        self.assertEqual(text, BATCH5_BLOCK, "batch-5 block must be batch-4 skin plus grown-horn wording")
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
        self.assertEqual(list(prompts), BATCH6_KEYS, "lab keys must be the batch-6 survey ladder in order")
        text, _ = TestKeechwahLabDescriptions().load_block()
        for i, key in enumerate(BATCH6_KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], BATCH6_SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {text}", f"{key} not exact composition")
            self.assertIn(entry["output"], (None, f"img/{key}.png"))
            self.assertEqual(list(entry["species_sources"].values()), [KEECHWAH_URL])

    def test_lab_workflows_family(self):
        import glob as _glob

        stems = [os.path.splitext(os.path.basename(p))[0] for p in _glob.glob("workflows/keechwahlab_*.json")]
        found = {s.removeprefix("keechwahlab_") for s in stems}
        self.assertEqual(found, set(BATCH6_KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts()
        for key in BATCH6_KEYS:
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
