import json
import os
import unittest

from scripts.build_arm_b import ADDENDUM, PROMPT_KEYS, parse_descriptions
from tests.test_arm_c import FRAME_C, MODEL_PATH
from tests.test_build_sheet_bible import RACE_URL, SLUG_RACE

LAB_DIR = "character-bible/sheet-test/gulgrim-lab"
LAB_DESC = os.path.join(LAB_DIR, "descriptions.md")
LAB_PROMPTS = os.path.join(LAB_DIR, "prompts.json")
KEYS = [f"gulgrim_g{i:02d}" for i in range(1, 5)]
SEEDS = [424242, 424243, 777001, 424244]
GULGRIM_URL = RACE_URL[SLUG_RACE["gulgrim"]]
# Batch 2: warhammer worn at the hip — batch-1 verdict was0/4 clean
# warhammers from the bare word `warhammer` (improvised grips, axe-head
# drift). Position is the single variable; future batches replace this
# constant with their revised block; the assertion below is the lab's
# wording ledger.
BATCH2_BLOCK = (
    "adult male hill dwarf cleric, short stocky, broad long white beard, heavy furs, "
    "frost-covered boots, his warhammer at his hip, standing well under five feet tall, "
    "broad and compact, holy symbol of Marthammor Du, exactly two arms"
)


class TestGulgrimLabDescriptions(unittest.TestCase):
    def load_block(self):
        self.assertTrue(os.path.exists(LAB_DESC), "gulgrim-lab/descriptions.md missing (author it first)")
        blocks = parse_descriptions(LAB_DESC)
        self.assertEqual(set(blocks), {"gulgrim"}, f"lab must hold exactly the gulgrim block, got {set(blocks)}")
        return blocks["gulgrim"]["text"], blocks["gulgrim"]["sources"]

    def test_baseline_block_is_arm_b_verbatim(self):
        text, sources = self.load_block()
        self.assertEqual(text, BATCH2_BLOCK, "block must be the pinned batch-2 wording")
        self.assertIn("character-bible/Sheets/Gulgrim.pdf", sources)
        self.assertIn(GULGRIM_URL, sources)
        self.assertTrue(any("bible.md locked chunks" in s for s in sources))


class TestGulgrimLabPrompts(unittest.TestCase):
    def load_prompts(self):
        self.assertTrue(os.path.exists(LAB_PROMPTS), "gulgrim-lab/prompts.json missing (run build_lab first)")
        with open(LAB_PROMPTS, encoding="utf-8") as f:
            return json.load(f)

    def test_lab_prompts_schema(self):
        prompts = self.load_prompts()
        self.assertEqual(list(prompts), KEYS, "lab keys must be the batch-1 ladder in order")
        for i, key in enumerate(KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {BATCH2_BLOCK}", f"{key} not exact composition")
            self.assertIn(entry["output"], (None, f"img/{key}.png"))
            self.assertEqual(list(entry["species_sources"].values()), [GULGRIM_URL])

    def test_lab_workflows_family(self):
        import glob as _glob

        stems = [os.path.splitext(os.path.basename(p))[0] for p in _glob.glob("workflows/gulgrimlab_*.json")]
        found = {s.removeprefix("gulgrimlab_") for s in stems}
        self.assertEqual(found, set(KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts()
        for key in KEYS:
            with open(f"workflows/gulgrimlab_{key}.json", encoding="utf-8") as f:
                g = json.load(f)
            seeds = [n["inputs"][k] for n in g.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})]
            self.assertEqual(set(seeds), {prompts[key]["seed"]}, f"gulgrimlab_{key} graph seed mismatch")
            saves = [n for n in g.values() if n["class_type"] == "SaveImage"]
            self.assertEqual(saves[0]["inputs"]["filename_prefix"], f"gulgrimlab_{key}")

    def test_builder_slug_override(self):
        # pins the build_lab generalization for a third slug: gulgrim builds cleanly
        import subprocess
        import sys
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/build_lab.py",
                 "--descriptions", LAB_DESC,
                 "--out-dir", tmp,
                 "--model-path", MODEL_PATH,
                 "--slug", "gulgrim",
                 "--seeds", "424242",
                 "--keys", "gulgrim_g01"],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(os.path.join(tmp, "prompts.json"), encoding="utf-8") as f:
                produced = json.load(f)
        self.assertEqual(list(produced), ["gulgrim_g01"])
        self.assertEqual(produced["gulgrim_g01"]["seed"], 424242)


if __name__ == "__main__":
    unittest.main()
