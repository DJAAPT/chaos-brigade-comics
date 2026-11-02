import glob
import json
import os
import re
import unittest

OUT_DIR = "character-bible/sheet-test"
PROMPTS = os.path.join(OUT_DIR, "prompts.json")
BIBLE_MD = os.path.join(OUT_DIR, "sheet-bible.md")
FRAME = "solo full-body portrait of a single character, plain background"
SEED = 424242
PROMPT_KEYS = [
    "character", "arm", "prompt", "frame", "species_sources", "seed",
    "model_hashes", "workflow", "output", "timestamp",
]
RACE_URL = {
    "Halfling": "https://www.dndbeyond.com/species/14-halfling",
    "Hill Dwarf": "https://www.dndbeyond.com/species/13-dwarf",
    "Tiefling": "https://www.dndbeyond.com/species/7-tiefling",
    "Wood Elf": "https://www.dndbeyond.com/species/3-elf",
    "Human": "https://www.dndbeyond.com/species/1-human",
}
SLUG_RACE = {
    "chip": "Human", "gulgrim": "Hill Dwarf", "keechwah": "Tiefling",
    "rocketcandy": "Human", "shade": "Halfling", "vadania": "Wood Elf",
}
MECHANICS_RE = re.compile(r"\b(Stealth|Saving Throw|Armor Class|Hit Points|Proficiency)\b|\w+ \+\d+")
FORBIDDEN_TOKENS = ["bible.md", "refs/", "gallery"]


class TestBuildSheetBible(unittest.TestCase):
    def load(self):
        self.assertTrue(os.path.exists(PROMPTS), "prompts.json missing (run build_sheet_bible first)")
        with open(PROMPTS, encoding="utf-8") as f:
            return json.load(f)

    def test_frame_first(self):
        for slug, entry in self.load().items():
            self.assertTrue(entry["prompt"].startswith(FRAME), f"{slug} does not open on frame")
            self.assertEqual(entry["prompt"].count(FRAME), 1, f"{slug} frame occurs !=1")

    def test_species_verbatim(self):
        with open(os.path.join(OUT_DIR, "data", "species.json"), encoding="utf-8") as f:
            species = json.load(f)
        prompts = self.load()
        self.assertIn("thick tails", species["7-tiefling"]["physical"])
        self.assertIn("thick tails", prompts["keechwah"]["prompt"])
        # every character's prompt carries the opening of its species physical text
        page_for = {"7-tiefling": "keechwah", "13-dwarf": "gulgrim", "3-elf": "vadania",
                    "14-halfling": "shade", "1-human": "chip"}
        for page, slug in page_for.items():
            anchor = species[page]["physical"][:40]
            self.assertIn(anchor, prompts[slug]["prompt"], f"{slug} missing physical anchor {anchor!r}")

    def test_sheet_verbatim(self):
        prompts = self.load()
        self.assertIn("Rapier", prompts["shade"]["prompt"])
        self.assertIn("Plate, +2", prompts["rocketcandy"]["prompt"])

    def test_no_mechanics_in_prompts(self):
        for slug, entry in self.load().items():
            m = MECHANICS_RE.search(entry["prompt"])
            self.assertIsNone(m, f"{slug} mechanics leaked: {m.group(0) if m else None!r}")

    def test_mechanics_pattern_catches_stat_forms(self):
        # stat-style modifiers must be detectable (any skill, not just the named terms)
        self.assertIsNotNone(MECHANICS_RE.search("made an Acrobatics +6 check"))
        self.assertIsNotNone(MECHANICS_RE.search("proficient in Stealth +6"))
        self.assertIsNotNone(MECHANICS_RE.search("Armor Class 16, Hit Points 44"))
        # enchanted item names are content the plan REQUIRES in prompts (Plate, +2),
        # and list joiners place them after ", " — they must not trip the filter
        self.assertIsNone(MECHANICS_RE.search("equipment: Plate, +2, Battleaxe, +3"))

    def test_no_local_reference_reads(self):
        for path in glob.glob("scripts/*.py"):
            with open(path, encoding="utf-8") as f:
                src = f.read()
            src = src.replace("sheet-bible.md", "")  # this task's own output, not the locked file
            for token in FORBIDDEN_TOKENS:
                self.assertNotIn(token, src, f"{path} references forbidden token {token!r}")

    def test_prompts_json_schema(self):
        prompts = self.load()
        self.assertEqual(set(prompts), {"chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"})
        for slug, entry in prompts.items():
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{slug} key mismatch")
            self.assertEqual(entry["arm"], "A")
            self.assertEqual(entry["seed"], SEED)
            self.assertEqual(entry["frame"], FRAME)
            # null before a run, the recorded path after (Task 6 fills it)
            self.assertIn(entry["output"], (None, f"img/{slug}.png"), f"{slug} output not null-or-recorded")
            self.assertEqual(
                list(entry["species_sources"].values()), [RACE_URL[SLUG_RACE[slug]]],
                f"{slug} species source mismatch",
            )
            self.assertEqual(entry["model_hashes"]["unet_name"], "flux3-image-klein-nvfp4.safetensors")
            self.assertRegex(entry["model_hashes"]["sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(entry["workflow"], "workflows/base_flux3.json")

    def test_sheet_bible_mirrors(self):
        self.assertTrue(os.path.exists(BIBLE_MD), "sheet-bible.md missing (run build_sheet_bible first)")
        with open(BIBLE_MD, encoding="utf-8") as f:
            md = f.read()
        for slug, entry in self.load().items():
            self.assertIn(entry["prompt"], md, f"{slug} prompt not mirrored in sheet-bible.md")
            self.assertIn(f"({slug})", md)

    def test_species_noise_not_in_prompts(self):
        # species chrome and setting lore must never reach a generated prompt
        for slug, entry in self.load().items():
            self.assertNotIn("Basic Rules (", entry["prompt"], f"{slug} prompt has source-line chrome")
            self.assertNotIn("Faer", entry["prompt"], f"{slug} prompt has setting lore")
            self.assertNotIn("Greyhawk", entry["prompt"], f"{slug} prompt has setting lore")


if __name__ == "__main__":
    unittest.main()
