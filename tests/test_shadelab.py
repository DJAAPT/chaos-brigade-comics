import json
import os
import unittest

from scripts.build_arm_b import ADDENDUM, PROMPT_KEYS, parse_descriptions
from tests.test_arm_c import FRAME_C
from tests.test_build_sheet_bible import RACE_URL, SLUG_RACE

LAB_DIR = "character-bible/sheet-test/shade-lab"
LAB_DESC = os.path.join(LAB_DIR, "descriptions.md")
LAB_PROMPTS = os.path.join(LAB_DIR, "prompts.json")
LAB_WORKFLOW_DIR = "workflows"
SEEDS = [424242, 424243, 777001, 314159]
KEYS = [f"shade_s{i}" for i in range(4)]
# Batch 6 ladder: s2 control seed + three historic S1 panel seeds
BATCH6_KEYS = ["shade_s2", "shade_s4", "shade_s5", "shade_s6"]
BATCH6_SEEDS = [777001, 1857761984156622644, 6120004243239096470, 8620240391160718909]
SHADE_URL = RACE_URL[SLUG_RACE["shade"]]
SHADE_CHUNK = (
    "young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown "
    "hair falling over and covering his ears, ears small and rounded beneath it, light stubble, "
    "no beard, warm brown eyes, subtle sly closed-mouth expression, worn dark linen shirt with "
    "rolled sleeves, scuffed brown leather vest, belt dagger at hips"
)
SCALED_CLAUSE = (
    "full-size adult human features scaled down uniformly, exactly the same head-to-body and "
    "ear-to-head proportions as a full-size grown man, he is a full-grown man who happens to "
    "stand three feet tall, enlarged to six feet he would be indistinguishable from an ordinary "
    "human man, small adult head, small low-profile human ears pinned flat against the skull, "
    "tucked beneath his hair below eye level, zero ear flair, small skull structure, sleek adult "
    "facial proportions, no pointed tips, no elf ears, no large ears, no protruding ears, "
    "no oversized head, no chibi or doll-like proportions"
)


class TestShadeLabDescriptions(unittest.TestCase):
    def load_block(self):
        self.assertTrue(os.path.exists(LAB_DESC), "shade-lab/descriptions.md missing (author it first)")
        blocks = parse_descriptions(LAB_DESC)
        self.assertEqual(set(blocks), {"shade"}, f"lab must hold exactly the shade block, got {set(blocks)}")
        return blocks["shade"]["text"], blocks["shade"]["sources"]

    def test_revised_block_pins_fix(self):
        text, sources = self.load_block()
        self.assertIn(SHADE_CHUNK, text, "Arm B shade chunk must appear verbatim")
        self.assertIn(SCALED_CLAUSE, text, "scaled-down clause with all four ear bans missing")
        # clause order: chunk -> scaled clause -> exactly two arms
        self.assertLess(text.index(SHADE_CHUNK), text.index(SCALED_CLAUSE))
        self.assertLess(text.index(SCALED_CLAUSE), text.index("exactly two arms"))
        self.assertEqual(text.count("exactly two arms"), 1)
        self.assertRegex(text, r"(?i)not a baby", "batch 4 showed a baby read — must be banned")
        self.assertRegex(text, r"(?i)not a toddler", "batch 4 showed a toddler read — must be banned")
        self.assertNotRegex(text, r"(?i)shield")
        self.assertIn(f"character-bible/Sheets/Shade.pdf", sources)
        self.assertIn(SHADE_URL, sources)
        self.assertTrue(any("bible.md locked chunks" in s for s in sources))

    def test_production_frame_c_export(self):
        try:
            from scripts.build_arm_b import FRAME_C as prod_frame
        except ImportError:
            self.fail("build_arm_b must export the FRAME_C constant for lab reuse")
        self.assertEqual(prod_frame, FRAME_C)


class TestShadeLabPrompts(unittest.TestCase):
    def load_prompts(self):
        self.assertTrue(os.path.exists(LAB_PROMPTS), "shade-lab/prompts.json missing (run build_shadelab first)")
        with open(LAB_PROMPTS, encoding="utf-8") as f:
            return json.load(f)

    def test_lab_prompts_schema(self):
        prompts = self.load_prompts()
        self.assertEqual(list(prompts), BATCH6_KEYS, "lab keys must be the batch-6 ladder in order")
        _, sources = TestShadeLabDescriptions().load_block()
        for i, key in enumerate(BATCH6_KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], BATCH6_SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertTrue(entry["prompt"].startswith(FRAME_C + " " + ADDENDUM), f"{key} frame/addendum order")
            self.assertIn(entry["output"], (None, f"img/{key}.png"), f"{key} output not null-or-recorded")
            self.assertEqual(list(entry["species_sources"].values()), [SHADE_URL])

    def test_prompt_is_exact_composition(self):
        text, _ = TestShadeLabDescriptions().load_block()
        for key, entry in self.load_prompts().items():
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {text}", f"{key} not exact composition")

    def test_custom_seeds_and_keys_override(self):
        # batch 6 shape: keep the s2 control seed, probe three new ones —
        # the builder must accept an explicit key/seed ladder
        import subprocess
        import sys
        import tempfile

        from tests.test_arm_c import MODEL_PATH

        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/build_shadelab.py",
                 "--descriptions", LAB_DESC,
                 "--out-dir", tmp,
                 "--model-path", MODEL_PATH,
                 "--seeds", "777001", "1857761984156622644",
                 "--keys", "shade_s2", "shade_s4"],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(os.path.join(tmp, "prompts.json"), encoding="utf-8") as f:
                produced = json.load(f)
        self.assertEqual(list(produced), ["shade_s2", "shade_s4"])
        self.assertEqual(produced["shade_s2"]["seed"], 777001)
        self.assertEqual(produced["shade_s4"]["seed"], 1857761984156622644)
        self.assertEqual(produced["shade_s4"]["arm"], "C")

    def test_build_one_honors_entry_seed(self):
        from scripts.build_sheet_workflows import build_one

        with open("workflows/base_flux3.json", encoding="utf-8") as f:
            base = json.load(f)
        graph = build_one(base, "some prompt", "x", seed=777001)
        seeds = [n["inputs"][k] for n in graph.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})]
        self.assertTrue(seeds)
        self.assertEqual(set(seeds), {777001}, "seed parameter not honored")
        graph_default = build_one(base, "some prompt", "x")
        seeds_default = [
            n["inputs"][k] for n in graph_default.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})
        ]
        self.assertEqual(set(seeds_default), {424242}, "default seed must stay 424242")
        # explicit None must coalesce to the default too (never write null into a graph)
        graph_none = build_one(base, "some prompt", "x", seed=None)
        seeds_none = [
            n["inputs"][k] for n in graph_none.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})
        ]
        self.assertEqual(set(seeds_none), {424242}, "explicit seed=None must fall back to 424242")

    def test_lab_workflows_family(self):
        import glob as _glob

        import re

        stems = [os.path.splitext(os.path.basename(p))[0] for p in _glob.glob("workflows/shadelab_*.json")]
        found = {s.removeprefix("shadelab_") for s in stems}
        self.assertEqual(found, set(BATCH6_KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts() if os.path.exists(LAB_PROMPTS) else None
        for key in BATCH6_KEYS:
            with open(f"workflows/shadelab_{key}.json", encoding="utf-8") as f:
                g = json.load(f)
            seeds = [n["inputs"][k] for n in g.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})]
            if prompts:
                self.assertEqual(set(seeds), {prompts[key]["seed"]}, f"shadelab_{key} graph seed mismatch")
            saves = [n for n in g.values() if n["class_type"] == "SaveImage"]
            self.assertEqual(saves[0]["inputs"]["filename_prefix"], f"shadelab_{key}")


if __name__ == "__main__":
    unittest.main()
