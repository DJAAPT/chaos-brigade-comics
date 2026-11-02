import json
import os
import unittest

SHEETS = "character-bible/sheet-test/data/sheets.json"
EXPECTED_SLUGS = {"chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"}
PHYSICAL_KEYS = ["gender", "age", "height", "weight", "hair", "skin", "eyes"]
DROP_KEYS = {"str", "dex", "hp", "ac", "skills"}


class TestExtractSheets(unittest.TestCase):
    def load_sheets(self):
        self.assertTrue(os.path.exists(SHEETS), "sheets.json missing (run extract_sheets first)")
        with open(SHEETS, encoding="utf-8") as f:
            return json.load(f)

    def test_roster_is_exactly_the_six_sheets(self):
        entries = self.load_sheets()
        self.assertEqual(set(entries), EXPECTED_SLUGS)

    def test_real_values_not_labels(self):
        shade = self.load_sheets()["shade"]
        self.assertEqual(shade["name"], "Shade")
        self.assertEqual(shade["race"], "Halfling")
        self.assertEqual(shade["class_level"], "Rogue 5")
        self.assertEqual(shade["background"], "Criminal")
        self.assertIn("Rapier", shade["equipment"])

    def test_physical_block_sparsity(self):
        entries = self.load_sheets()
        self.assertEqual(entries["chip"]["physical"]["gender"], "Male")
        self.assertEqual(
            entries["keechwah"]["physical"],
            {k: "(no sheet text)" for k in PHYSICAL_KEYS},
        )

    def test_boilerplate_flags(self):
        entries = self.load_sheets()
        self.assertIsNotNone(entries["vadania"]["appearance"])
        self.assertIs(entries["vadania"]["appearance"]["boilerplate"], True)
        self.assertIsNotNone(entries["keechwah"]["backstory"])
        self.assertIs(entries["keechwah"]["backstory"]["boilerplate"], True)
        self.assertIsNotNone(entries["shade"]["backstory"])
        self.assertIs(entries["shade"]["backstory"]["boilerplate"], False)

    def test_drop_list_keys_absent(self):
        entries = self.load_sheets()
        for slug, entry in entries.items():
            leaked = DROP_KEYS & set(entry)
            self.assertFalse(leaked, f"{slug} leaked drop-list keys: {leaked}")


if __name__ == "__main__":
    unittest.main()
