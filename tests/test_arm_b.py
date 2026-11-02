import json
import os
import re
import unittest

from scripts.build_arm_b import parse_descriptions
from tests.test_build_sheet_bible import MECHANICS_RE, RACE_URL, SLUG_RACE

DESCRIPTIONS = "character-bible/sheet-test/arm_b/descriptions.md"
SLUGS = {"chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"}


class TestArmBDescriptions(unittest.TestCase):
    def load_blocks(self):
        self.assertTrue(os.path.exists(DESCRIPTIONS), "descriptions.md missing (author it first)")
        blocks = parse_descriptions(DESCRIPTIONS)
        self.assertTrue(blocks, "no '## Name (slug)' blocks parsed from descriptions.md")
        return blocks

    def test_six_blocks_with_sources(self):
        blocks = self.load_blocks()
        self.assertEqual(set(blocks), SLUGS)
        for slug, block in blocks.items():
            name = block["name"]
            self.assertTrue(block["text"], f"{slug} has empty description text")
            sources = block["sources"]
            self.assertIn(f"character-bible/Sheets/{name}.pdf", sources, f"{slug} sources missing its PDF")
            self.assertIn(RACE_URL[SLUG_RACE[slug]], sources, f"{slug} sources missing its species URL")
            self.assertTrue(
                any("bible.md locked chunks" in s for s in sources),
                f"{slug} sources missing the locked-chunks line",
            )

    def test_no_shield_in_descriptions(self):
        for slug, block in self.load_blocks().items():
            self.assertNotRegex(block["text"], r"(?i)shield", f"{slug} description mentions a shield")

    def test_win_phrases(self):
        blocks = self.load_blocks()
        shade = blocks["shade"]["text"]
        self.assertRegex(shade, r"(?i)adult", "shade must say adult")
        self.assertRegex(shade, r"(?i)not a child", "shade must carry the NOT a child win")
        self.assertRegex(blocks["keechwah"]["text"], r"(?i)no wings", "keechwah must carry NO wings")
        self.assertRegex(blocks["vadania"]["text"], r"(?i)not female", "vadania must carry the NOT female win")
        for slug, block in blocks.items():
            self.assertRegex(block["text"], r"(?i)exactly two arms", f"{slug} missing exactly two arms")

    def test_locked_chunks_verbatim(self):
        # Plan Task 1: locked chunks are copied verbatim (the sole approved
        # edit is Gulgrim's shield removal under the newer composition rule).
        expected = {
            "shade": "young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair falling over and covering his ears, ears small and rounded beneath it, light stubble, no beard, warm brown eyes, subtle sly closed-mouth expression, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, belt dagger at hips",
            "rocketcandy": "adult male human paladin, short brown hair light stubble, shining plate armor with gold phoenix/eagle crest on chest, red cape, exactly two arms",
            "keechwah": "adult male tiefling warlock, deep red skin, long curly black hair, goatee, large curved horns, glowing purple eyes, male facial features, dark blue/gold robes, gold jewelry, NO wings",
            "gulgrim": "adult male hill dwarf cleric, short stocky, broad long white beard, heavy furs, frost-covered boots, warhammer",
            "chip": "adult male human druid, wild long white hair and white beard, green/brown fur garb, holding wooden staff (HE holds it, never Vadania)",
            "vadania": "adult male wood elf ranger, long brown hair, green eyes, pointed ears, masculine jaw stubble, green cloak, longbow on back, short swords at hips, scar on shoulder",
        }
        blocks = self.load_blocks()
        for slug, chunk in expected.items():
            self.assertIn(chunk, blocks[slug]["text"], f"{slug} locked chunk not present verbatim")
        # Gulgrim specifically: the chunk appears minus exactly the shield segment
        self.assertNotIn("large round shield with holy rune", blocks["gulgrim"]["text"])

    def test_production_parser_and_builder(self):
        # suite must exercise the real parser and entry builder, not test copies
        from scripts.build_arm_b import ADDENDUM, FRAME, PROMPT_KEYS, build_entry

        blocks = parse_descriptions(DESCRIPTIONS)
        self.assertEqual(set(blocks), SLUGS)
        for slug, block in blocks.items():
            self.assertTrue(block["text"], f"{slug} production parser got empty text")
        dummy = {"unet_name": "flux3-image-klein-nvfp4.safetensors", "sha256": "0" * 64}
        entry = build_entry("keechwah", blocks["keechwah"], dummy, "T")
        self.assertEqual(list(entry.keys()), PROMPT_KEYS)
        self.assertTrue(entry["prompt"].startswith(f"{FRAME} {ADDENDUM} {blocks['keechwah']['text']}"))
        self.assertEqual(entry["arm"], "B")
        self.assertEqual(entry["seed"], 424242)

    def test_no_mechanics(self):
        for slug, block in self.load_blocks().items():
            m = MECHANICS_RE.search(block["text"])
            self.assertIsNone(m, f"{slug} mechanics leaked: {m.group(0) if m else None!r}")


FRAME = "solo full-body portrait of a single character, plain background"
ADDENDUM = "standing neutral pose, both arms clearly visible, no shield, nothing held across the body"
PROMPTS_B = "character-bible/sheet-test/arm_b/prompts.json"


class TestArmBPrompts(unittest.TestCase):
    def load_prompts(self):
        self.assertTrue(os.path.exists(PROMPTS_B), "arm_b/prompts.json missing (run build_arm_b first)")
        with open(PROMPTS_B, encoding="utf-8") as f:
            return json.load(f)

    def test_prompts_schema(self):
        from tests.test_build_sheet_bible import PROMPT_KEYS

        prompts = self.load_prompts()
        self.assertEqual(set(prompts), SLUGS)
        for slug, entry in prompts.items():
            self.assertEqual(list(entry.keys()), PROMPT_KEYS, f"{slug} key mismatch")
            self.assertEqual(entry["arm"], "B")
            self.assertEqual(entry["seed"], 424242)
            self.assertEqual(entry["frame"], FRAME)
            self.assertTrue(entry["prompt"].startswith(FRAME + " " + ADDENDUM), f"{slug} frame/addendum order")
            # null before a run, the recorded path after (the runner fills it)
            self.assertIn(entry["output"], (None, f"img/{slug}.png"), f"{slug} output not null-or-recorded")
            self.assertEqual(entry["workflow"], "workflows/base_flux3.json")

    def test_prompt_is_exact_composition(self):
        # prompt == frame + addendum + authored block, verbatim — proves the
        # Task-1 block bans carry into the built prompts unchanged
        blocks = parse_descriptions(DESCRIPTIONS)
        for slug, entry in self.load_prompts().items():
            expected = f"{FRAME} {ADDENDUM} {blocks[slug]['text']}"
            self.assertEqual(entry["prompt"], expected, f"{slug} prompt is not the exact composition")

    def test_composition_and_win_phrases(self):
        for slug, entry in self.load_prompts().items():
            prompt = entry["prompt"]
            # the plan's shield ban, minus the addendum's own negation sentence
            remainder = prompt.replace(ADDENDUM, "")
            self.assertNotRegex(remainder, r"(?i)shield", f"{slug} prompt mentions a shield outside the addendum")
            self.assertRegex(prompt, r"(?i)exactly two arms", f"{slug} missing exactly two arms")
            m = MECHANICS_RE.search(remainder)
            self.assertIsNone(m, f"{slug} mechanics leaked: {m.group(0) if m else None!r}")
        shade = self.load_prompts()["shade"]["prompt"]
        self.assertRegex(shade, r"(?i)adult")
        self.assertRegex(shade, r"(?i)not a child")
        self.assertRegex(self.load_prompts()["keechwah"]["prompt"], r"(?i)no wings")

    def test_sources_match_blocks(self):
        blocks = parse_descriptions(DESCRIPTIONS)
        for slug, entry in self.load_prompts().items():
            species_url = next(
                (s for s in blocks[slug]["sources"] if s.startswith("https://www.dndbeyond.com/species/")),
                None,
            )
            self.assertIsNotNone(species_url, f"{slug} block has no species URL")
            self.assertEqual(list(entry["species_sources"].values()), [species_url], f"{slug} source mismatch")


if __name__ == "__main__":
    unittest.main()
