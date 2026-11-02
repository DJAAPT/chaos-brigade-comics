import json
import os
import subprocess
import sys
import tempfile
import unittest

from scripts.build_arm_b import parse_descriptions
from tests.test_arm_b import ADDENDUM, DESCRIPTIONS, FRAME as FRAME_B, SLUGS
from tests.test_build_sheet_bible import PROMPT_KEYS

FRAME_C = (
    "solo full-body portrait of a single character, head-to-toe full body with feet visible "
    "and empty space above the head, stationary camera at a fixed distance, plain background"
)
INSERTED_CLAUSE = (
    ", head-to-toe full body with feet visible and empty space above the head, "
    "stationary camera at a fixed distance"
)
PROMPTS_C = "character-bible/sheet-test/arm_c/prompts.json"
PROMPTS_B = "character-bible/sheet-test/arm_b/prompts.json"
MODEL_PATH = r"C:\DEV\ComfyUI\models\diffusion_models\flux3-image-klein-nvfp4.safetensors"


class TestArmCFraming(unittest.TestCase):
    def test_frame_clause_exact(self):
        # the inserted clause is the ONLY difference between the two frames
        self.assertEqual(FRAME_C.replace(INSERTED_CLAUSE, ""), FRAME_B)
        self.assertIn(INSERTED_CLAUSE, FRAME_C)
        self.assertTrue(FRAME_C.startswith("solo full-body portrait of a single character,"))

    def load_prompts(self):
        self.assertTrue(os.path.exists(PROMPTS_C), "arm_c/prompts.json missing (run build with --frame first)")
        with open(PROMPTS_C, encoding="utf-8") as f:
            return json.load(f)

    def test_prompts_schema(self):
        prompts = self.load_prompts()
        self.assertEqual(set(prompts), SLUGS)
        for slug, entry in prompts.items():
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{slug} key mismatch")
            self.assertEqual(entry["arm"], "C")
            self.assertEqual(entry["seed"], 424242)
            self.assertEqual(entry["frame"], FRAME_C)
            self.assertTrue(entry["prompt"].startswith(FRAME_C + " " + ADDENDUM), f"{slug} frame/addendum order")
            # lifecycle-aware: null before a run, recorded path after (rounds 1+2 pattern)
            self.assertIn(entry["output"], (None, f"img/{slug}.png"), f"{slug} output not null-or-recorded")
            self.assertEqual(entry["workflow"], "workflows/base_flux3.json")

    def test_prompt_is_exact_composition(self):
        blocks = parse_descriptions(DESCRIPTIONS)
        for slug, entry in self.load_prompts().items():
            expected = f"{FRAME_C} {ADDENDUM} {blocks[slug]['text']}"
            self.assertEqual(entry["prompt"], expected, f"{slug} prompt is not the exact composition")

    def test_blocks_identical_to_arm_b(self):
        # single-variable proof: stripping each arm's frame leaves byte-equal remainders
        with open(PROMPTS_B, encoding="utf-8") as f:
            prompts_b = json.load(f)
        prompts_c = self.load_prompts()
        for slug in SLUGS:
            remainder_b = prompts_b[slug]["prompt"][len(FRAME_B) + 1:]
            remainder_c = prompts_c[slug]["prompt"][len(FRAME_C) + 1:]
            self.assertEqual(remainder_c, remainder_b, f"{slug} remainder differs from Arm B — blocks/addendum drifted")

    def test_default_build_matches_arm_b(self):
        # builder WITHOUT --frame must reproduce Arm B prompts (timestamp exempt)
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/build_arm_b.py",
                 "--descriptions", DESCRIPTIONS,
                 "--out-dir", tmp,
                 "--model-path", MODEL_PATH],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(os.path.join(tmp, "prompts.json"), encoding="utf-8") as f:
                produced = json.load(f)
        with open(PROMPTS_B, encoding="utf-8") as f:
            committed = json.load(f)
        self.assertEqual(set(produced), set(committed))
        for slug in committed:
            a = dict(produced[slug])
            b = dict(committed[slug])
            # runtime fields — differ by construction (fresh build vs recorded run)
            for runtime in ("timestamp", "output"):
                a.pop(runtime), b.pop(runtime)
            self.assertEqual(a, b, f"{slug} default build differs from committed Arm B")


if __name__ == "__main__":
    unittest.main()
