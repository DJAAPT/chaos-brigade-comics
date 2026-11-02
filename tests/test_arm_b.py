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


if __name__ == "__main__":
    unittest.main()
