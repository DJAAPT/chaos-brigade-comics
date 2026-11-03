import json
import os
import unittest

LAB_DIR = "character-bible/lineup-lab"
LAB_README = os.path.join(LAB_DIR, "README.md")
LAB_DESC = os.path.join(LAB_DIR, "descriptions.md")
LAB_SLOTS = os.path.join(LAB_DIR, "slots.json")
LAB_PROMPTS = os.path.join(LAB_DIR, "prompts.json")


def ledger_has_batch_table():
    if not os.path.exists(LAB_README):
        return False
    with open(LAB_README, encoding="utf-8") as f:
        text = f.read()
    return ("batch1" in text.lower() or "batch 1" in text.lower()) and "wall" in text.lower()


def prompts_keys():
    with open(LAB_PROMPTS, encoding="utf-8") as f:
        return list(json.load(f))


def slots_has_six_with_shade_3ft():
    with open(LAB_SLOTS, encoding="utf-8") as f:
        slots = json.load(f)
    if isinstance(slots, dict) and "slots" in slots:
        slots = slots["slots"]
    if not isinstance(slots, list) or len(slots) != 6:
        return False
    shade = [s for s in slots if s.get("character") == "shade"]
    if len(shade) != 1:
        return False
    height = str(shade[0].get("height", "")).lower()
    return "3" in height


class TestLineupLabLedger(unittest.TestCase):
    def test_lineuplab_ledger_exists(self):
        self.assertTrue(os.path.exists(LAB_README), "lineup-lab/README.md missing (author it first)")
        self.assertTrue(os.path.exists(LAB_DESC), "lineup-lab/descriptions.md missing")
        self.assertTrue(os.path.exists(LAB_SLOTS), "lineup-lab/slots.json missing")
        self.assertTrue(os.path.exists(LAB_PROMPTS), "lineup-lab/prompts.json missing")
        self.assertTrue(ledger_has_batch_table(), "README must hold a batch table mentioning batch 1 + wall")
        self.assertEqual(prompts_keys(), ["wall_empty", "wall_shade_s1"])
        self.assertTrue(slots_has_six_with_shade_3ft(), "slots.json must hold six slots with Shade at 3ft")


class TestLineupLabWorkflows(unittest.TestCase):
    def test_lineuplab_workflows_family(self):
        import glob as _glob
        stems = {__import__("os").path.splitext(__import__("os").path.basename(p))[0]
                 for p in _glob.glob("workflows/lineuplab_*.json")}
        self.assertEqual(stems, {"lineuplab_wall_empty", "lineuplab_wall_shade"},
                         f"lab workflow set mismatch: {stems}")
        with open("workflows/lineuplab_wall_empty.json", encoding="utf-8") as f:
            wall = json.load(f)
        wall_text = json.dumps(wall)
        self.assertNotIn("LoadImage", wall_text, "empty wall must not load a reference image")
        with open("workflows/lineuplab_wall_shade.json", encoding="utf-8") as f:
            shade = json.load(f)
        shade_text = json.dumps(shade)
        self.assertIn("lineup_shade_ref.png", shade_text, "insert must ref lineup Shade copy of approved PNG")
        self.assertIn("ReferenceMultiLatent", shade_text)


if __name__ == "__main__":
    unittest.main()
