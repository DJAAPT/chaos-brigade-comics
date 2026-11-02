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
        stems = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob("workflows/sheettest_*.json")]
        # round-1 family only: its slugs contain no underscore; the arm_b_/arm_c_
        # families (sheettest_b_<slug>, sheettest_c_<slug>) have their own tests
        found = {s.removeprefix("sheettest_") for s in stems if "_" not in s.removeprefix("sheettest_")}
        self.assertEqual(found, SLUGS, f"workflow set mismatch: {found}")

    def test_arm_b_family_exactly_six(self):
        stems = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob("workflows/sheettest_b_*.json")]
        found = {s.removeprefix("sheettest_b_") for s in stems}
        self.assertEqual(found, SLUGS, f"Arm B workflow set mismatch: {found}")

    def test_default_prefix_round1_unchanged(self):
        # Regression guard: build_one without the new prefix argument must
        # keep round-1 behavior byte-identical (filename_prefix sheettest_<slug>).
        from scripts.build_sheet_workflows import build_one

        with open(BASE, encoding="utf-8") as f:
            base = json.load(f)
        graph = build_one(base, "some prompt", "shade")
        saves = [n for n in graph.values() if n["class_type"] == "SaveImage"]
        self.assertEqual(saves[0]["inputs"]["filename_prefix"], "sheettest_shade")

    def test_prefixed_build_uses_given_prefix(self):
        from scripts.build_sheet_workflows import build_one

        with open(BASE, encoding="utf-8") as f:
            base = json.load(f)
        graph = build_one(base, "some prompt", "shade", prefix="sheettest_b_")
        saves = [n for n in graph.values() if n["class_type"] == "SaveImage"]
        self.assertEqual(saves[0]["inputs"]["filename_prefix"], "sheettest_b_shade")

    def test_arm_c_family_exactly_six(self):
        stems = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob("workflows/sheettest_c_*.json")]
        found = {s.removeprefix("sheettest_c_") for s in stems}
        self.assertEqual(found, SLUGS, f"Arm C workflow set mismatch: {found}")
        with open("workflows/sheettest_c_shade.json", encoding="utf-8") as f:
            g = json.load(f)
        saves = [n for n in g.values() if n["class_type"] == "SaveImage"]
        self.assertEqual(saves[0]["inputs"]["filename_prefix"], "sheettest_c_shade")

    def test_round1_defaults_untouched(self):
        # The default CLI must reproduce round-1 workflows byte-for-byte in a
        # temp dir (filenames, prefixes, and graph content all identical).
        import subprocess
        import sys
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "scripts/build_sheet_workflows.py",
                 "--base", BASE, "--prompts", "character-bible/sheet-test/prompts.json",
                 "--out-dir", tmp],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            for slug in SLUGS:
                produced = os.path.join(tmp, f"sheettest_{slug}.json")
                committed = os.path.join("workflows", f"sheettest_{slug}.json")
                self.assertTrue(os.path.exists(produced), f"missing {produced}")
                with open(produced, "rb") as a, open(committed, "rb") as b:
                    self.assertEqual(a.read(), b.read(), f"{slug} default output differs from committed round-1")

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
