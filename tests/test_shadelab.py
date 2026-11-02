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
SHADE_URL = RACE_URL[SLUG_RACE["shade"]]
SHADE_CHUNK = (
    "young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown "
    "hair falling over and covering his ears, ears small and rounded beneath it, light stubble, "
    "no beard, warm brown eyes, subtle sly closed-mouth expression, worn dark linen shirt with "
    "rolled sleeves, scuffed brown leather vest, belt dagger at hips"
)
SCALED_CLAUSE = (
    "full-size adult human features scaled down uniformly, exactly the same head-to-body and "
    "ear-to-head proportions as a full-size grown man, head one-seventh of total body height, "
    "small adult head, small rounded human ears mostly tucked "
    "under his hair, lying flat against the sides of his head below eye level, no pointed tips, "
    "no elf ears, no large ears, no protruding ears, no oversized head, no chibi or doll-like proportions"
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
        self.assertEqual(list(prompts), KEYS, "lab keys must be shade_s0..s3 in order")
        _, sources = TestShadeLabDescriptions().load_block()
        for i, key in enumerate(KEYS):
            entry = prompts[key]
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{key} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], SEEDS[i], f"{key} seed mismatch")
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertTrue(entry["prompt"].startswith(FRAME_C + " " + ADDENDUM), f"{key} frame/addendum order")
            self.assertIn(entry["output"], (None, f"img/{key}.png"), f"{key} output not null-or-recorded")
            self.assertEqual(list(entry["species_sources"].values()), [SHADE_URL])

    def test_prompt_is_exact_composition(self):
        text, _ = TestShadeLabDescriptions().load_block()
        for key, entry in self.load_prompts().items():
            self.assertEqual(entry["prompt"], f"{FRAME_C} {ADDENDUM} {text}", f"{key} not exact composition")

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
        self.assertEqual(found, set(KEYS), f"lab workflow set mismatch: {found}")
        prompts = self.load_prompts() if os.path.exists(LAB_PROMPTS) else None
        for key in KEYS:
            with open(f"workflows/shadelab_{key}.json", encoding="utf-8") as f:
                g = json.load(f)
            seeds = [n["inputs"][k] for n in g.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})]
            if prompts:
                self.assertEqual(set(seeds), {prompts[key]["seed"]}, f"shadelab_{key} graph seed mismatch")
            saves = [n for n in g.values() if n["class_type"] == "SaveImage"]
            self.assertEqual(saves[0]["inputs"]["filename_prefix"], f"shadelab_{key}")


if __name__ == "__main__":
    unittest.main()
