"""Completion gate for the sheet-test run.

complete() is True only when the prompts.json roster is exactly the six
sheet-test characters, every entry records output == img/<slug>.png, and
every one of those six PNGs exists at 1344x768. The CLI runs the same
validator: it prints a table and exits 0 on COMPLETE, else lists what is
missing/mismatched and exits 1. There is no path where a partial,
duplicated, or wrong-roster run certifies as complete.
"""
import argparse
import json
import os
import struct
import sys

EXPECTED_DIMS = (1344, 768)
ROSTER = ("chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania")


def parse_ihdr(path: str) -> tuple:
    """Return (width, height) from the PNG IHDR at fixed offsets 16..24."""
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24:
        raise ValueError(f"{path}: too short for a PNG header")
    return struct.unpack(">II", header[16:24])


def problems(prompts: dict, img_dir: str) -> list:
    """Every reason this run is not complete (empty list == COMPLETE)."""
    found = []
    if set(prompts) != set(ROSTER):
        missing = sorted(set(ROSTER) - set(prompts))
        extra = sorted(set(prompts) - set(ROSTER))
        found.append(f"roster mismatch — missing: {missing or 'none'}, unexpected: {extra or 'none'}")
        return found

    for slug in ROSTER:
        output = prompts[slug].get("output")
        expected = f"img/{slug}.png"
        if not output:
            found.append(f"{slug}: output not recorded")
            continue
        if output != expected:
            found.append(f"{slug}: output {output!r} != {expected!r}")
            continue
        path = os.path.join(img_dir, os.path.basename(output))
        if not os.path.exists(path):
            found.append(f"{slug}: missing file {path}")
            continue
        try:
            dims = parse_ihdr(path)
        except ValueError as exc:
            found.append(f"{slug}: {exc}")
            continue
        if dims != EXPECTED_DIMS:
            found.append(f"{slug}: dims {dims[0]}x{dims[1]} != {EXPECTED_DIMS[0]}x{EXPECTED_DIMS[1]}")
    return found


def complete(prompts: dict, img_dir: str) -> bool:
    """True only for the full six-character run with correct recorded PNGs."""
    return not problems(prompts, img_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--img", required=True)
    args = parser.parse_args()

    with open(args.prompts, encoding="utf-8") as f:
        prompts = json.load(f)

    issues = problems(prompts, args.img)
    if issues:
        print("INCOMPLETE")
        for line in issues:
            print(f"  - {line}")
        sys.exit(1)

    print("COMPLETE")
    print(f"{'character':<14} {'output':<24} {'dims':<10}")
    for slug in ROSTER:
        path = os.path.join(args.img, os.path.basename(prompts[slug]["output"]))
        w, h = parse_ihdr(path)
        print(f"{slug:<14} {prompts[slug]['output']:<24} {w}x{h}")


if __name__ == "__main__":
    main()
