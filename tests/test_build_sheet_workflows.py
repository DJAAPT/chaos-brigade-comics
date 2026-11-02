import glob
import json
import os
import unittest

SLUGS = {"chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"}
BASE = "workflows/base_flux3.json"
PROMPTS = "character-bible/sheet-test/prompts.json"
SEED = 424242


def wf_path(slug):
    return f"workflows/sheettest_{slug}.json"


class TestBuildSheetWorkflows(unittest.TestCase):
    def test_exactly_six(self):
        found = {
            os.path.splitext(os.path.basename(p))[0].removeprefix("sheettest_")
            for p in glob.glob("workflows/sheettest_*.json")
        }
        self.assertEqual(found, SLUGS, f"workflow set mismatch: {found}")

    def test_prompt_swap_and_untouched_graph(self):
        files = glob.glob("workflows/sheettest_*.json")
        self.assertTrue(files, "no sheettest_*.json workflow files (run build_sheet_workflows first)")

        with open(BASE, encoding="utf-8") as f:
            base = json.load(f)
        base_shape = {node_id: node["class_type"] for node_id, node in base.items()}
        with open(PROMPTS, encoding="utf-8") as f:
            prompts = json.load(f)

        for slug in sorted(SLUGS):
            with open(wf_path(slug), encoding="utf-8") as f:
                raw = f.read()
            g = json.loads(raw)

            # graph structure unchanged (node ids and class types identical to base)
            shape = {node_id: node["class_type"] for node_id, node in g.items()}
            self.assertEqual(shape, base_shape, f"{slug} graph structure drifted from base")

            texts = [n["inputs"]["text"] for n in g.values() if isinstance(n.get("inputs", {}).get("text"), str)]
            self.assertIn(prompts[slug]["prompt"], texts, f"{slug} prompt not swapped in")
            self.assertNotIn("{{PROMPT}}", raw, f"{slug} sentinel left behind")
            self.assertNotIn("cinematic fantasy film still", raw, f"{slug} still carries old S1 text")

            self.assertTrue(
                any(n["inputs"].get("unet_name") == "flux3-image-klein-nvfp4.safetensors" for n in g.values()),
                f"{slug} unet changed",
            )

            saves = [n for n in g.values() if n["class_type"] == "SaveImage"]
            self.assertEqual(len(saves), 1, f"{slug} SaveImage count != 1")
            self.assertEqual(saves[0]["inputs"]["filename_prefix"], f"sheettest_{slug}")

            seeds = [
                n["inputs"].get(key, "missing")
                for n in g.values()
                for key in ("seed", "noise_seed")
                if key in n.get("inputs", {})
            ]
            self.assertTrue(seeds, f"{slug} no seed inputs found")
            self.assertEqual(seeds, [SEED] * len(seeds), f"{slug} seed not pinned: {seeds}")


if __name__ == "__main__":
    unittest.main()
