"""Completion gate for the sheet-test run.

complete() is True only when every prompts.json entry has a recorded
output and its PNG exists at 1344x768. The CLI prints a table and
exits 0 on COMPLETE, else lists what is missing/mismatched and exits 1.
"""
import argparse
import json
import os
import struct
import sys

EXPECTED_DIMS = (1344, 768)


def parse_ihdr(path: str) -> tuple:
    """Return (width, height) from the PNG IHDR at fixed offsets 16..24."""
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24:
        raise ValueError(f"{path}: too short for a PNG header")
    return struct.unpack(">II", header[16:24])


def complete(prompts: dict, img_dir: str) -> bool:
    """True when all six entries have outputs pointing at correct PNGs."""
    for entry in prompts.values():
        output = entry.get("output")
        if not output:
            return False
        path = os.path.join(img_dir, os.path.basename(output))
        if not os.path.exists(path):
            return False
        try:
            if parse_ihdr(path) != EXPECTED_DIMS:
                return False
        except ValueError:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--img", required=True)
    args = parser.parse_args()

    with open(args.prompts, encoding="utf-8") as f:
        prompts = json.load(f)

    problems = []
    for slug in sorted(prompts):
        entry = prompts[slug]
        output = entry.get("output")
        if not output:
            problems.append(f"{slug}: output not recorded")
            continue
        path = os.path.join(args.img, os.path.basename(output))
        if not os.path.exists(path):
            problems.append(f"{slug}: missing file {path}")
            continue
        try:
            dims = parse_ihdr(path)
        except ValueError as exc:
            problems.append(f"{slug}: {exc}")
            continue
        if dims != EXPECTED_DIMS:
            problems.append(f"{slug}: dims {dims[0]}x{dims[1]} != {EXPECTED_DIMS[0]}x{EXPECTED_DIMS[1]}")

    if problems:
        print("INCOMPLETE")
        for line in problems:
            print(f"  - {line}")
        sys.exit(1)

    print("COMPLETE")
    print(f"{'character':<14} {'output':<24} {'dims':<10}")
    for slug in sorted(prompts):
        path = os.path.join(args.img, os.path.basename(prompts[slug]["output"]))
        w, h = parse_ihdr(path)
        print(f"{slug:<14} {prompts[slug]['output']:<24} {w}x{h}")


if __name__ == "__main__":
    main()
