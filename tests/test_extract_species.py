import json
import os
import unittest

SPECIES = "character-bible/sheet-test/data/species.json"
BANNED = ["Rollback Post", "Posted May", "Male Infernal Names"]


class TestExtractSpecies(unittest.TestCase):
    def load_species(self):
        self.assertTrue(os.path.exists(SPECIES), "species.json missing (run extract_species first)")
        with open(SPECIES, encoding="utf-8") as f:
            return json.load(f)

    def all_text(self, entry):
        parts = [entry.get("physical", ""), entry.get("age_size", "")]
        parts.extend(entry.get("sections", {}).values())
        return " ".join(parts)

    def test_tiefling_physical(self):
        phys = self.load_species()["7-tiefling"]["physical"]
        self.assertIn("thick tails", phys)
        self.assertIn("horns", phys)
        self.assertIn("no visible sclera", phys)

    def test_excludes_noise(self):
        for slug, entry in self.load_species().items():
            blob = self.all_text(entry)
            for banned in BANNED:
                self.assertNotIn(banned, blob, f"{slug} contains noise string {banned!r}")

    def test_subrace_sections_addressable(self):
        species = self.load_species()
        dwarf_keys = species["13-dwarf"]["sections"].keys()
        self.assertTrue(any("Hill Dwarf" in k for k in dwarf_keys), f"no Hill Dwarf section: {list(dwarf_keys)}")
        elf_keys = species["3-elf"]["sections"].keys()
        self.assertTrue(any("Wood Elf" in k for k in elf_keys), f"no Wood Elf section: {list(elf_keys)}")

    def test_fiction_quotes_excluded(self):
        # Spec drops "quoted fiction blurbs": the page epigraphs must never
        # reach physical/age_size, even when their dialogue hits keywords.
        species = self.load_species()
        tiefling = species["7-tiefling"]
        self.assertTrue(
            tiefling["physical"].startswith("Tieflings are derived from human bloodlines"),
            f"tiefling physical does not open on the Infernal Bloodline paragraph: {tiefling['physical'][:80]!r}",
        )
        self.assertNotIn("glared", tiefling["physical"])
        self.assertNotIn("Yer late", species["13-dwarf"]["physical"])


if __name__ == "__main__":
    unittest.main()
