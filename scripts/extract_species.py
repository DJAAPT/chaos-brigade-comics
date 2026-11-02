"""Fetch and extract official D&D Beyond species details.

--fetch downloads the five legacy species pages to
character-bible/sheet-test/data/sources/ (live step, exits 3 on any
non-200 or suspiciously small response). Without --fetch, cached HTML
is parsed into species.json: verbatim physical-description paragraphs,
Age/Size trait paragraphs, and an addressable sections map — article
body only, no name lists, no history/lore fluff beyond what the
physical rules select, no forum comments.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

PAGES = {
    "7-tiefling": "https://www.dndbeyond.com/species/7-tiefling",
    "13-dwarf": "https://www.dndbeyond.com/species/13-dwarf",
    "3-elf": "https://www.dndbeyond.com/species/3-elf",
    "14-halfling": "https://www.dndbeyond.com/species/14-halfling",
    "1-human": "https://www.dndbeyond.com/species/1-human",
}
DEFAULT_SOURCES = os.path.join("character-bible", "sheet-test", "data", "sources")
DEFAULT_OUT = os.path.join("character-bible", "sheet-test", "data", "species.json")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MIN_FETCH_BYTES = 50_000

SKIP_MARKERS = re.compile(r"Rollback|Posted \w+ \d|Names:|Basic Rules \(\d{4}\)")
PHYS_HEADING = re.compile(r"description|appearance|bloodline|physique", re.I)
AGE_SIZE_HEADING = re.compile(r"^(Age|Size)$", re.I)
# Official description chapters per page: the paragraphs under these headings
# are the species physique prose (stature/skin/build openers). Selection is
# heading-grounded — the old >=2-keyword sweep swallowed setting/ethnicity
# lore wherever body words co-occurred (reviewer's finding, reproduced).
CHAPTER_HEADINGS = {
    "7-tiefling": ("Infernal Bloodline",),
    "13-dwarf": ("Short and Stout",),
    "3-elf": ("Slender and Graceful",),
    "14-halfling": ("Small and Practical",),
    "1-human": ("A Broad Spectrum",),
}
# Setting-lore sentences are dropped from section text (spec drops
# history/culture/lore; subrace sections keep their trait sentence only).
LORE_SENTENCE_RE = re.compile(
    r"(?i)Faer[uû]n|Krynn|Greyhawk|Dragonlance|Forgotten Realms|This category includes"
)


def fetch(sources_dir: str) -> None:
    """Download every species page into sources_dir; exit 3 on any failure."""
    os.makedirs(sources_dir, exist_ok=True)
    failures = []
    for slug, url in PAGES.items():
        dest = os.path.join(sources_dir, f"{slug}.html")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                status = getattr(resp, "status", 200)
                body = resp.read()
        except Exception as exc:  # noqa: BLE001 - report and fail the batch
            failures.append(f"{slug}: fetch error {exc}")
            continue
        if status != 200:
            failures.append(f"{slug}: HTTP {status}")
        elif len(body) < MIN_FETCH_BYTES:
            failures.append(f"{slug}: only {len(body)} bytes")
        else:
            with open(dest, "wb") as f:
                f.write(body)
            print(f"fetched {slug}: {len(body)} bytes -> {dest}")
    if failures:
        for line in failures:
            print(f"FAILED {line}", file=sys.stderr)
        sys.exit(3)


def _clean_heading(text: str) -> str:
    """Drop the legacy-badge clutter DDB appends to old subrace headings."""
    return re.sub(r"\s*Legacy This doesn't reflect.*$", "", text).strip()


def parse(sources_dir: str, out_path: str) -> dict:
    """Parse cached HTML into species.json (see module docstring).

    Walks the article from its <h1> to the Comments heading, tracking the
    current heading. Paragraphs (verbatim) are classified into age_size,
    physical, and the per-heading sections map; skip-marked paragraphs
    (forum noise, name lists) are dropped everywhere.
    """
    from bs4 import BeautifulSoup

    result = {}
    for slug in PAGES:
        path = os.path.join(sources_dir, f"{slug}.html")
        if not os.path.exists(path):
            print(f"missing cached page: {path} (run --fetch first)", file=sys.stderr)
            sys.exit(3)

        soup = BeautifulSoup(open(path, "rb").read(), "html.parser")
        h1 = soup.find("h1")
        if h1 is None:
            print(f"no <h1> in {path}", file=sys.stderr)
            sys.exit(3)

        url = PAGES[slug]
        chapters = CHAPTER_HEADINGS.get(slug, ())
        physical_parts, age_size_parts = [], []
        sections = {}
        current_heading = None
        current_key = None

        for el in h1.find_all_next(["h2", "h3", "h4", "h5", "p"]):
            if el.name in ("h2", "h3", "h4", "h5"):
                heading = el.get_text(" ", strip=True)
                if heading.lower() == "comments":
                    break
                current_heading = _clean_heading(heading)
                current_key = current_heading
                sections.setdefault(current_key, [])
                continue
            # <p> — fiction epigraphs live in blockquotes; spec drops them
            if el.find_parent("blockquote") is not None:
                continue
            text = el.get_text(" ", strip=True)
            if not text or SKIP_MARKERS.search(text):
                continue
            if current_heading is not None and AGE_SIZE_HEADING.match(current_heading):
                age_size_parts.append(text)
            elif current_heading is not None and (
                PHYS_HEADING.search(current_heading) or current_heading in chapters
            ):
                physical_parts.append(text)
            if current_key is not None:
                sections[current_key].append(text)

        result[slug] = {
            "url": url,
            "physical": " ".join(physical_parts),
            "age_size": " ".join(age_size_parts),
            "sections": {
                k: _strip_lore_sentences(" ".join(v)) for k, v in sections.items()
            },
        }
    return result


def _strip_lore_sentences(text: str) -> str:
    """Drop sentences carrying setting/lore proper nouns; keep the rest."""
    kept = [s for s in re.split(r"(?<=[.!?])\s+", text) if not LORE_SENTENCE_RE.search(s)]
    return " ".join(kept)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="download the five pages, then exit")
    parser.add_argument("--sources", default=DEFAULT_SOURCES, help="cached HTML directory")
    parser.add_argument("--out", default=DEFAULT_OUT, help="output species.json path")
    args = parser.parse_args()

    if args.fetch:
        fetch(args.sources)
        return
    result = parse(args.sources, args.out)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(result)} species to {args.out}")


if __name__ == "__main__":
    main()
