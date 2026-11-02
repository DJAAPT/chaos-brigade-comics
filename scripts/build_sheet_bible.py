"""Build the Arm A sheet bible and prompt audit log.

Assembles one prompt per character from verbatim sources only: the
neutral frame, the official DDB species text (physical + Age/Size +
subrace section), and the character's sheet block (race, class, background,
filled physical values, equipment, weapons, description fields with a
boilerplate flag). Writes prompts.json (spec's nine keys, output null)
and sheet-bible.md mirroring each prompt with its sources.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

FRAME = "solo full-body portrait of a single character, plain background"
SEED = 424242
UNET_NAME = "flux3-image-klein-nvfp4.safetensors"
WORKFLOW = "workflows/base_flux3.json"
NO_TEXT = "(no sheet text)"

PROMPT_KEYS = [
    "character", "arm", "prompt", "frame", "species_sources", "seed",
    "model_hashes", "workflow", "output", "timestamp",
]
RACE_TO_PAGE = {
    "Halfling": "14-halfling",
    "Hill Dwarf": "13-dwarf",
    "Tiefling": "7-tiefling",
    "Wood Elf": "3-elf",
    "Human": "1-human",
}
SUBRACE_SECTIONS = {
    "Hill Dwarf": ("13-dwarf", "Hill Dwarf"),
    "Wood Elf": ("3-elf", "Wood Elf"),
}
PHYSICAL_ORDER = ["gender", "age", "height", "weight", "hair", "skin", "eyes"]
DESCRIPTION_ORDER = ["appearance", "backstory", "ideals", "bonds", "flaws", "personality"]


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def species_text(sheet, species) -> str:
    """Verbatim species detail: physical, Age/Size sentences, subrace section."""
    race = sheet["race"]
    if race not in RACE_TO_PAGE:
        print(f"race {race!r} has no species page mapping", file=sys.stderr)
        sys.exit(2)
    page = species[RACE_TO_PAGE[race]]
    parts = [page["physical"], page["age_size"]]
    if race in SUBRACE_SECTIONS:
        _, prefix = SUBRACE_SECTIONS[race]
        section = next((v for k, v in page["sections"].items() if prefix in k), "")
        parts.append(section)
    return " ".join(p for p in parts if p)


def sheet_block(sheet) -> str:
    parts = [sheet["race"], sheet["class_level"], sheet["background"]]
    parts.extend(
        f"{key} {sheet['physical'][key]}"
        for key in PHYSICAL_ORDER
        if sheet["physical"].get(key) != NO_TEXT
    )
    if sheet["equipment"]:
        parts.append(", ".join(sheet["equipment"]))
    if sheet["weapons"]:
        parts.append(", ".join(sheet["weapons"]))
    for key in DESCRIPTION_ORDER:
        field = sheet.get(key)
        if not field:
            continue
        text = field["text"] + (" (boilerplate)" if field.get("boilerplate") else "")
        parts.append(text)
    return ", ".join(parts)


def build_entry(slug, sheet, species, model_hashes, timestamp) -> dict:
    prompt = " ".join([FRAME, species_text(sheet, species), sheet_block(sheet)])
    url = species[RACE_TO_PAGE[sheet["race"]]]["url"]
    entry = {
        "character": slug,
        "arm": "A",
        "prompt": prompt,
        "frame": FRAME,
        "species_sources": {RACE_TO_PAGE[sheet["race"]]: url},
        "seed": SEED,
        "model_hashes": model_hashes,
        "workflow": WORKFLOW,
        "output": None,
        "timestamp": timestamp,
    }
    assert list(entry.keys()) == PROMPT_KEYS
    return entry


def write_markdown(entries, sheets, species, path):
    lines = ["# Sheet-Test — Arm A prompt blocks (generated from sheets + DDB species pages)", ""]
    for slug, entry in entries.items():
        race = sheets[slug]["race"]
        page = RACE_TO_PAGE[race]
        lines += [
            f"## {sheets[slug]['name']} ({slug})",
            "",
            "Prompt:",
            "",
            entry["prompt"],
            "",
            "Sources:",
            "",
            f"- character-bible/Sheets/{slug.capitalize()}.pdf",
            f"- {species[page]['url']}",
            "",
        ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, help="data dir holding sheets.json/species.json")
    parser.add_argument("--out-dir", required=True, help="sheet-test output dir")
    parser.add_argument("--model-path", required=True, help="local flux3 unet file to hash")
    args = parser.parse_args()

    with open(os.path.join(args.data, "sheets.json"), encoding="utf-8") as f:
        sheets = json.load(f)
    with open(os.path.join(args.data, "species.json"), encoding="utf-8") as f:
        species = json.load(f)
    if not os.path.exists(args.model_path):
        print(f"model file missing: {args.model_path}", file=sys.stderr)
        sys.exit(2)

    model_hashes = {"unet_name": UNET_NAME, "sha256": sha256_of(args.model_path)}
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entries = {
        slug: build_entry(slug, sheets[slug], species, model_hashes, timestamp)
        for slug in sorted(sheets)
    }

    os.makedirs(args.out_dir, exist_ok=True)
    prompts_path = os.path.join(args.out_dir, "prompts.json")
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")
    write_markdown(entries, sheets, species, os.path.join(args.out_dir, "sheet-bible.md"))
    print(f"wrote {len(entries)} prompts to {prompts_path} and sheet-bible.md")


if __name__ == "__main__":
    main()
