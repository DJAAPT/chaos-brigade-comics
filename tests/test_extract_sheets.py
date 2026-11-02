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

    def test_spell_attacks_and_currency_filtered(self):
        entries = self.load_sheets()
        # representative leaks the reviewer found in the committed data
        banned = ["Chill Touch", "Fire Bolt", "Ray of Frost", "Shillelagh",
                  "Starry Wisp", "Unarmed Strike", "1-pound silver bars"]
        for slug, entry in entries.items():
            for kind in ("equipment", "weapons"):
                for value in entry[kind]:
                    self.assertNotIn(value, banned, f"{slug} {kind} kept non-visible entry {value!r}")

    def test_no_carried_spell_names_survive(self):
        # re-read the real spell fields and prove no equipment/weapons value collides
        for pdf_name, slug in [("Chip", "chip"), ("Keechwah", "keechwah")]:
            from pypdf import PdfReader

            spells = set()
            reader = PdfReader(os.path.join("character-bible", "Sheets", f"{pdf_name}.pdf"))
            for page in reader.pages:
                annots = page.get("/Annots")
                annots = annots.get_object() if hasattr(annots, "get_object") else annots
                if not annots:
                    continue
                for ref in annots:
                    obj = ref.get_object()
                    name, val = obj.get("/T"), obj.get("/V")
                    if name is not None and val not in (None, "") and str(name).lower().startswith("spellname"):
                        spells.add(str(val).strip().lower())
            entry = self.load_sheets()[slug]
            for kind in ("equipment", "weapons"):
                for value in entry[kind]:
                    base = value.lower()
                    hit = next((s for s in spells if base.startswith(s)), None)
                    self.assertIsNone(hit, f"{slug} {kind} carries spell {value!r} ~ {hit!r}")

    def test_equipment_has_no_page_restart_duplicates(self):
        entries = self.load_sheets()
        for slug, entry in entries.items():
            for kind in ("equipment", "weapons"):
                values = entry[kind]
                self.assertEqual(len(values), len(set(values)), f"{slug} {kind} has duplicates: {values}")


if __name__ == "__main__":
    unittest.main()
