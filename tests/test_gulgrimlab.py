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
# Batch 3 ladder: seed 424244 RETIRED (grey hands persisted across two
# wordings — batches 1+2 verdict); 424245 promoted into gulgrim_g04
# (verified disjoint from every ladder in the repo). Wording frozen at
# BATCH2_BLOCK.
SEEDS = [424242, 424243, 777001, 424245]
# Batch 4 ladder: 20-seed survey on the frozen batch-2 block (wording
# proven 4/4 on weapons in batch 2, ladder cleaned in batch 3) — hit-rate
# read before the next wording variable. Master seed 20261121, harvest
# script C:/Users/Andrew/AppData/Local/Temp/harvest_gulgrim04.py, verified
# disjoint from all 319 previously used seeds repo-wide.
BATCH4_KEYS = [f"gulgrim_r{i:02d}" for i in range(1, 21)]
BATCH4_SEEDS = [750162285, 1206558873, 1496924836, 352959242, 1449593620, 316783734,
                17335413, 776038280, 688472172, 1552965976, 1505368845, 733124982,
                705257192, 1563623009, 1690805504, 1508036947, 1477778073, 495603372,
                1051377175, 1756671735]
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
        self.assertEqual(list(prompts), BATCH4_KEYS, "lab keys must be the batch-4 survey ladder in order")
        for i, key in enumerate(BATCH4_KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], BATCH4_SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {BATCH2_BLOCK}", f"{key} not exact composition")
            self.assertIn(entry["output"], (None, f"img/{key}.png"))
            self.assertEqual(list(entry["species_sources"].values()), [GULGRIM_URL])

    def test_batch3_ladder_retired_seed(self):
        # pins the batch-3 retirement: the control ladder must have
        # dropped 424244 for 424245 at gulgrim_g04, wording frozen
        import subprocess
        import sys
        import tempfile

        self.assertEqual(SEEDS, [424242, 424243, 777001, 424245], "batch-3 ladder keeps the replacement seed")
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/build_lab.py",
                 "--descriptions", LAB_DESC,
                 "--out-dir", tmp,
                 "--model-path", MODEL_PATH,
                 "--slug", "gulgrim",
                 "--seeds", "424242", "424243", "777001", "424245",
                 "--keys", "gulgrim_g01", "gulgrim_g02", "gulgrim_g03", "gulgrim_g04"],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            import json as _json
            with open(os.path.join(tmp, "prompts.json"), encoding="utf-8") as f:
                produced = _json.load(f)
        self.assertNotIn(424244, [e["seed"] for e in produced.values()], "retired seed must not return")

    def test_lab_workflows_family(self):
        import glob as _glob

        stems = [os.path.splitext(os.path.basename(p))[0] for p in _glob.glob("workflows/gulgrimlab_*.json")]
        found = {s.removeprefix("gulgrimlab_") for s in stems}
        self.assertEqual(found, set(BATCH4_KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts()
        for key in BATCH4_KEYS:
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
