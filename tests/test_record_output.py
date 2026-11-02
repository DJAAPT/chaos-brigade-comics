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

    def test_complete_rejects_empty_and_partial_rosters(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(mod.complete({}, tmp), "empty roster must never be complete")
            four = {s: dict(output=f"img/{s}.png") for s in SLUGS[:4]}
            for s in SLUGS[:4]:
                make_png(os.path.join(tmp, f"{s}.png"))
            self.assertFalse(mod.complete(four, tmp), "four-entry roster must never be complete")

    def test_complete_rejects_wrong_roster(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            prompts = base_prompts()
            prompts["biggins"] = prompts.pop("shade")
            prompts["biggins"]["output"] = "img/biggins.png"
            for slug in SLUGS:
                make_png(os.path.join(tmp, f"{slug}.png"))
            make_png(os.path.join(tmp, "biggins.png"))
            self.assertFalse(mod.complete(prompts, tmp), "roster other than the six must never be complete")

    def test_default_roster_unchanged(self):
        # without an explicit roster, a four-entry lab-shaped run must NOT certify
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            four = {f"shade_s{i}": {"output": f"img/shade_s{i}.png"} for i in range(4)}
            for i in range(4):
                make_png(os.path.join(tmp, f"shade_s{i}.png"))
            self.assertFalse(mod.complete(four, tmp), "default roster must stay the exact six")

    def test_custom_roster_gates_lab(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        roster = tuple(f"shade_s{i}" for i in range(4))
        with tempfile.TemporaryDirectory() as tmp:
            prompts = {f"shade_s{i}": {"output": f"img/shade_s{i}.png"} for i in range(4)}
            for i in range(4):
                make_png(os.path.join(tmp, f"shade_s{i}.png"))
            self.assertTrue(mod.complete(prompts, tmp, roster=roster), "lab roster should certify a full lab run")
            prompts["shade_s2"]["output"] = None
            self.assertFalse(mod.complete(prompts, tmp, roster=roster), "missing output must fail lab gate")

    def test_empty_roster_never_certifies(self):
        # same false-positive class as round 1's Critical: an empty run must
        # never be complete, however the roster is spelled
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(mod.complete({}, tmp, roster=()), "empty prompts + empty roster must fail")
            self.assertFalse(mod.complete({}, tmp), "empty prompts on default roster must fail")
            issues = mod.problems({}, tmp, roster=())
            self.assertTrue(issues and any("roster" in i for i in issues), "empty roster must yield a roster problem")

    def test_complete_rejects_shared_output(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            prompts = base_prompts()
            for slug in SLUGS:
                make_png(os.path.join(tmp, f"{slug}.png"))
                prompts[slug]["output"] = "img/chip.png"  # every entry points at chip's file
            make_png(os.path.join(tmp, "chip.png"))
            self.assertFalse(mod.complete(prompts, tmp), "shared/duplicated outputs must never be complete")

    def test_complete_requires_output_path_per_slug(self):
        mod = self.import_module("scripts.verify_sheettest", "scripts/verify_sheettest.py")
        with tempfile.TemporaryDirectory() as tmp:
            prompts = base_prompts()
            for slug in SLUGS:
                make_png(os.path.join(tmp, f"{slug}.png"))
            prompts["shade"]["output"] = "img/chip.png"
            self.assertFalse(mod.complete(prompts, tmp), "output path not matching its slug must fail")


if __name__ == "__main__":
    unittest.main()
