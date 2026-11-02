import copy
import json
import os
import struct
import sys
import tempfile
import unittest

SLUGS = ["chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"]


def make_png(path, width=1344, height=768):
    """Write a minimal PNG-signature + IHDR prefix good enough for parse_ihdr."""
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")          # signature, offset 0..7
        f.write(b"\x00\x00\x00\x0dIHDR")        # length + type, offset 8..15
        f.write(struct.pack(">II", width, height))  # width/height, offset 16..23


def base_prompts(all_outputs=True):
    prompts = {}
    for slug in SLUGS:
        prompts[slug] = {
            "output": f"img/{slug}.png" if all_outputs else None,
            "timestamp": "old",
        }
    return prompts


class ImportGuard(unittest.TestCase):
    module = None

    def import_module(self, name, path):
        if not os.path.exists(path):
            self.fail(f"{path} missing (Task 6 not implemented yet)")
        import importlib

        return importlib.import_module(name)


class TestRecordOutput(ImportGuard):
    def test_record_output_updates_entry(self):
        mod = self.import_module("scripts.record_output", "scripts/record_output.py")
        prompts = base_prompts()
        before = copy.deepcopy(prompts)
        updated = mod.record_output(prompts, "shade", "img/shade.png", "2026-11-01T12:00:00+00:00")
        self.assertEqual(updated["shade"]["output"], "img/shade.png")
        self.assertEqual(updated["shade"]["timestamp"], "2026-11-01T12:00:00+00:00")
        for slug in SLUGS:
            if slug != "shade":
                self.assertEqual(updated[slug], before[slug], f"{slug} was mutated")

    def test_record_output_rejects_unknown_character(self):
        mod = self.import_module("scripts.record_output", "scripts/record_output.py")
        with self.assertRaises(KeyError):
            mod.record_output(base_prompts(), "biggins", "img/biggins.png", "ts")


class TestVerifySheettest(ImportGuard):
    def test_png_header_parse(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "x.png")
            make_png(path, 1344, 768)
            self.assertEqual(mod.parse_ihdr(path), (1344, 768))

    def test_requires_all_six_before_complete(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            # five PNGs, six outputs -> incomplete
            prompts = base_prompts(all_outputs=False)
            for slug in SLUGS[:5]:
                prompts[slug]["output"] = f"img/{slug}.png"
                make_png(os.path.join(tmp, f"{slug}.png"))
            self.assertFalse(mod.complete(prompts, tmp))

            # six PNGs at 1344x768, six outputs -> complete
            prompts = base_prompts()
            for slug in SLUGS:
                make_png(os.path.join(tmp, f"{slug}.png"))
            self.assertTrue(mod.complete(prompts, tmp))

            # wrong dimensions -> incomplete
            make_png(os.path.join(tmp, "shade.png"), 768, 1344)
            self.assertFalse(mod.complete(prompts, tmp))

    def test_complete_rejects_null_output(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            prompts = base_prompts()
            for slug in SLUGS:
                make_png(os.path.join(tmp, f"{slug}.png"))
            prompts["chip"]["output"] = None
            self.assertFalse(mod.complete(prompts, tmp))


if __name__ == "__main__":
    unittest.main()
