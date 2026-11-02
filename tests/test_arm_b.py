import json
import os
import re
import unittest

from tests.test_build_sheet_bible import MECHANICS_RE, RACE_URL, SLUG_RACE

DESCRIPTIONS = "character-bible/sheet-test/arm_b/descriptions.md"
SLUGS = {"chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"}


def parse_descriptions(path):
    """Return {slug: {"name": str, "text": str, "sources": [str]}} from the
    authored markdown: '## Name (slug)' heading, one paragraph, Sources block."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    blocks = {}
    sections = re.split(r"(?=^## )", raw, flags=re.M)
    for section in sections:
        lines = section.splitlines()
        if not lines:
            continue
        m = re.match(r"^## (.+) \((\w+)\)$", lines[0].rstrip("\r"))
        if not m:
            continue
        name, slug = m.group(1), m.group(2)
        body = "\n".join(lines[1:])
        if "Sources:" in body:
            text_part, sources_part = body.split("Sources:", 1)
        else:
            text_part, sources_part = body, ""
        sources = [ln.strip()[2:].strip() for ln in sources_part.splitlines() if ln.strip().startswith("- ")]
        blocks[slug] = {"name": name, "text": text_part.strip(), "sources": sources}
    return blocks


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
        for slug, block in blocks.items():
            self.assertRegex(block["text"], r"(?i)exactly two arms", f"{slug} missing exactly two arms")

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
