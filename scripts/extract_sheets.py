"""Extract character data from exported DDB sheet PDFs.

The printable-sheet PDFs carry their visible text as form labels only;
the real values live in widget annotations (/T name, /V value). This
script reads those widgets and writes a schema-fixed sheets.json whose
text values are verbatim, with absent fields rendered as "(no sheet
text)" and description fields flagged boilerplate when they match
known stock DDB prose.
"""
import argparse
import glob
import json
import os
import re
import sys

EXPECTED_SLUGS = {"chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania"}
NO_TEXT = "(no sheet text)"
WINDOW = 40

SCALAR_FIELDS = {
    "CharacterName": "name",
    "RACE": "race",
    "CLASS  LEVEL": "class_level",
    "BACKGROUND": "background",
    "ALIGNMENT": "alignment",
    "FAITH": "faith",
}
PHYSICAL_FIELDS = {
    "GENDER": "gender",
    "AGE": "age",
    "HEIGHT": "height",
    "WEIGHT": "weight",
    "HAIR": "hair",
    "SKIN": "skin",
    "EYES": "eyes",
}
DESCRIPTION_FIELDS = {
    "Appearance": "appearance",
    "Backstory": "backstory",
    "Ideals": "ideals",
    "Bonds": "bonds",
    "Flaws": "flaws",
    "Personality": "personality",
}
EQ_RE = re.compile(r"Eq Name\d*\Z")
WPN_RE = re.compile(r"Wpn Name ?\d*\Z")
SPELL_FIELD_RE = re.compile(r"spellname", re.I)
CURRENCY_RE = re.compile(
    r"(?i)(^|,\s*)\s*[\d.]+\s*[- ]\s*pound\b|\b(silver|gold|copper|electrum|platinum)\s+(bars?|coins?|pieces?)\b"
)
DENY_EXACT = {"unarmed strike"}


def is_visible_item(value, spells):
    """Spec: worn/visible equipment only — no carried spell attacks, no currency.

    `spells` is the character's own spellName field set (normalized lowercase);
    an item is dropped when its value starts with one of those names at a
    word boundary (kills cantrip attack rows like "Chill Touch").
    """
    lowered = value.lower().strip()
    if lowered in DENY_EXACT:
        return False
    if CURRENCY_RE.search(value):
        return False
    for spell in spells:
        if re.match(re.escape(spell) + r"\b", lowered):
            return False
    return True


def dedupe(values):
    """Order-preserving unique — the PDF repeats inventory pages under
    restarted field numbering, which would otherwise duplicate entries."""
    return list(dict.fromkeys(values))


def iter_widget_fields(pdf_path):
    """Yield (field_name, value) for every filled widget annotation."""
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    for page in reader.pages:
        annots = page.get("/Annots")
        annots = annots.get_object() if hasattr(annots, "get_object") else annots
        if not annots:
            continue
        for ref in annots:
            obj = ref.get_object()
            if str(obj.get("/Subtype", "")) != "/Widget":
                continue
            name = obj.get("/T")
            value = obj.get("/V")
            if name is None or value in (None, ""):
                continue
            yield str(name), str(value)


_APOSTROPHES = str.maketrans({c: "'" for c in "\u2018\u2019\u201a\u201b\u02bc\u00b4\u0060\u2032"})


def normalize(text):
    """Lowercase, collapse whitespace, and unify apostrophe variants so
    typographic quotes from the PDF match ASCII stock markers."""
    return re.sub(r"\s+", " ", text).translate(_APOSTROPHES).strip().lower()


def _collect_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _collect_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from _collect_strings(value)


def build_corpus(out_path):
    """Normalized stock-prose corpus: marker file + species bodies (if any)."""
    parts = []
    markers = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock_markers.txt")
    if os.path.exists(markers):
        with open(markers, encoding="utf-8") as f:
            parts.append(normalize(f.read()))
    species_path = os.path.join(os.path.dirname(out_path), "species.json")
    if os.path.exists(species_path):
        with open(species_path, encoding="utf-8") as f:
            species = json.load(f)
        parts.append(normalize(" ".join(_collect_strings(species))))
    return " ".join(parts)


def is_boilerplate(text, corpus):
    """True when a 40-char normalized window of the text occurs in the corpus."""
    if not corpus:
        return False
    norm = normalize(text)
    if len(norm) < WINDOW:
        return False
    return any(norm[i : i + WINDOW] in corpus for i in range(len(norm) - WINDOW + 1))


def extract_pdf(pdf_path, corpus):
    scalars = {}
    physical = {}
    descriptions = {}
    equipment = []
    weapons = []
    spells = set()

    for name, value in iter_widget_fields(pdf_path):
        if name in SCALAR_FIELDS:
            scalars[SCALAR_FIELDS[name]] = value
        elif name in PHYSICAL_FIELDS:
            physical[PHYSICAL_FIELDS[name]] = value
        elif name in DESCRIPTION_FIELDS:
            descriptions[DESCRIPTION_FIELDS[name]] = value
        elif SPELL_FIELD_RE.match(name):
            spell = value.strip().lower().split(" [")[0].strip()
            if spell:
                spells.add(spell)
        elif EQ_RE.fullmatch(name):
            equipment.append(value)
        elif WPN_RE.fullmatch(name):
            weapons.append(value)

    equipment = dedupe(v for v in equipment if is_visible_item(v, spells))
    weapons = dedupe(v for v in weapons if is_visible_item(v, spells))

    entry = {key: scalars.get(key, NO_TEXT) for key in SCALAR_FIELDS.values()}
    entry["physical"] = {key: physical.get(key, NO_TEXT) for key in PHYSICAL_FIELDS.values()}
    for field in DESCRIPTION_FIELDS.values():
        raw = descriptions.get(field)
        entry[field] = (
            None if raw is None else {"text": raw, "boilerplate": is_boilerplate(raw, corpus)}
        )
    entry["equipment"] = equipment
    entry["weapons"] = weapons
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", required=True, help="directory of sheet PDFs")
    parser.add_argument("--out", required=True, help="output sheets.json path")
    args = parser.parse_args()

    pdfs = sorted(glob.glob(os.path.join(args.src, "*.pdf")))
    if not pdfs:
        print(f"no PDFs found in {args.src}", file=sys.stderr)
        sys.exit(2)
    slugs = {os.path.splitext(os.path.basename(p))[0].lower() for p in pdfs}
    if slugs != EXPECTED_SLUGS:
        print(f"expected exactly {sorted(EXPECTED_SLUGS)}, found {sorted(slugs)}", file=sys.stderr)
        sys.exit(2)

    corpus = build_corpus(args.out)
    result = {
        os.path.splitext(os.path.basename(p))[0].lower(): extract_pdf(p, corpus) for p in pdfs
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(result)} characters to {args.out}")


if __name__ == "__main__":
    main()
