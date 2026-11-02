"""Function-level tests: exercise the pipeline implementations directly.

The other suites verify committed artifacts; these call the actual
functions against the real inputs (PDFs, cached HTML, base graph) with
all outputs going to temporary directories, so a regression in a script
cannot hide behind a stale artifact.
"""
import copy
import json
import os
import tempfile
import unittest

BIBLEREF = "workflows/bibleref_a_origseed.json"
PINNED_BASE = "workflows/base_flux3.json"
SOURCES = os.path.join("character-bible", "sheet-test", "data", "sources")
SHADE_PDF = os.path.join("character-bible", "Sheets", "Shade.pdf")
DUMMY_HASHES = {"unet_name": "flux3-image-klein-nvfp4.safetensors", "sha256": "0" * 64}


class TestPrepareFlux3BaseFunction(unittest.TestCase):
    def test_prepare_from_real_source(self):
        from scripts import prepare_flux3_base

        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "base.json")
            node_id = prepare_flux3_base.prepare(BIBLEREF, out)
            g = json.load(open(out, encoding="utf-8"))
        texts = [n["inputs"].get("text") for n in g.values() if "text" in n.get("inputs", {})]
        self.assertEqual(texts.count("{{PROMPT}}"), 1)
        self.assertEqual(g[node_id]["inputs"]["text"], "{{PROMPT}}")
        # rig untouched by preparation
        src = json.load(open(BIBLEREF, encoding="utf-8"))
        self.assertEqual(
            {k: v["class_type"] for k, v in g.items()},
            {k: v["class_type"] for k, v in src.items()},
        )


class TestExtractSheetsFunctions(unittest.TestCase):
    def test_extract_pdf_from_real_sheet(self):
        from scripts import extract_sheets

        entry = extract_sheets.extract_pdf(SHADE_PDF, corpus="")
        self.assertEqual(entry["name"], "Shade")
        self.assertEqual(entry["race"], "Halfling")
        self.assertEqual(entry["class_level"], "Rogue 5")
        self.assertIn("Rapier", entry["equipment"])

    def test_visible_item_filter(self):
        from scripts import extract_sheets

        self.assertFalse(extract_sheets.is_visible_item("Chill Touch", {"chill touch"}))
        self.assertFalse(extract_sheets.is_visible_item("Unarmed Strike", set()))
        self.assertFalse(extract_sheets.is_visible_item("1-pound silver bars", set()))
        self.assertTrue(extract_sheets.is_visible_item("Plate, +2", set()))
        self.assertTrue(extract_sheets.is_visible_item("Leather", {"chill touch"}))

    def test_dedupe_is_order_preserving(self):
        from scripts import extract_sheets

        self.assertEqual(extract_sheets.dedupe(["a", "b", "a", "c", "b"]), ["a", "b", "c"])


class TestExtractSpeciesFunction(unittest.TestCase):
    def test_parse_from_real_cached_sources(self):
        from scripts import extract_species

        result = extract_species.parse(SOURCES, os.path.join(tempfile.gettempdir(), "unused.json"))
        self.assertEqual(set(result), set(extract_species.PAGES))
        self.assertIn("thick tails", result["7-tiefling"]["physical"])
        self.assertIn("broad and compact", result["13-dwarf"]["physical"])
        for entry in result.values():
            blob = entry["physical"] + entry["age_size"] + " ".join(entry["sections"].values())
            self.assertNotIn("Basic Rules (", blob)


class TestBuildSheetBibleFunction(unittest.TestCase):
    def test_build_entry_from_real_data(self):
        from scripts import build_sheet_bible

        sheets = json.load(open(os.path.join("character-bible", "sheet-test", "data", "sheets.json"), encoding="utf-8"))
        species = json.load(open(os.path.join("character-bible", "sheet-test", "data", "species.json"), encoding="utf-8"))
        entry = build_sheet_bible.build_entry("keechwah", sheets["keechwah"], species, DUMMY_HASHES, "T")
        self.assertEqual(list(entry.keys()), build_sheet_bible.PROMPT_KEYS)
        self.assertTrue(entry["prompt"].startswith(build_sheet_bible.FRAME))
        self.assertIn("thick tails", entry["prompt"])
        self.assertIn("Tiefling, Warlock 5", entry["prompt"])
        self.assertIsNone(entry["output"])
        self.assertEqual(entry["seed"], 424242)


class TestBuildSheetWorkflowsFunction(unittest.TestCase):
    def test_build_one_from_real_base(self):
        from scripts import build_sheet_workflows

        base = json.load(open(PINNED_BASE, encoding="utf-8"))
        graph = build_sheet_workflows.build_one(base, "test prompt text", "shade")
        raw = json.dumps(graph)
        self.assertNotIn("{{PROMPT}}", raw)
        self.assertIn("test prompt text", raw)
        self.assertEqual(
            {k: v["class_type"] for k, v in graph.items()},
            {k: v["class_type"] for k, v in base.items()},
        )
        seeds = [n["inputs"][k] for n in graph.values() for k in ("seed", "noise_seed") if k in n.get("inputs", {})]
        self.assertTrue(seeds)
        self.assertEqual(set(seeds), {424242})
        saves = [n for n in graph.values() if n["class_type"] == "SaveImage"]
        self.assertEqual(saves[0]["inputs"]["filename_prefix"], "sheettest_shade")


if __name__ == "__main__":
    unittest.main()
