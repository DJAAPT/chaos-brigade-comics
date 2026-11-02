"""Build the Arm B (round 2) merged-description prompts.

Reads ONLY the authored descriptions.md (frame + composition addendum +
merged block per character) and writes arm_b/prompts.json in round 1's
nine-key audit schema with arm "B". No other input — merged wins reach
prompts solely through the authored file.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

FRAME = "solo full-body portrait of a single character, plain background"
FRAME_C = (
    "solo full-body portrait of a single character, head-to-toe full body with feet visible "
    "and empty space above the head, stationary camera at a fixed distance, plain background"
)
ADDENDUM = "standing neutral pose, both arms clearly visible, no shield, nothing held across the body"
UNet_NAME = "flux3-image-klein-nvfp4.safetensors"
WORKFLOW = "workflows/base_flux3.json"
SEED = 424242
SLUGS = ("chip", "gulgrim", "keechwah", "rocketcandy", "shade", "vadania")
PROMPT_KEYS = [
    "character", "arm", "prompt", "frame", "species_sources", "seed",
    "model_hashes", "workflow", "output", "timestamp",
]


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_descriptions(path: str) -> dict:
    """{slug: {"name": str, "text": str, "sources": [str]}} from the markdown."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    blocks = {}
    for section in re.split(r"(?=^## )", raw, flags=re.M):
        lines = section.splitlines()
        if not lines:
            continue
        m = re.match(r"^## (.+) \((\w+)\)$", lines[0].rstrip("\r"))
        if not m:
            continue
        name, slug = m.group(1), m.group(2)
        body = "\n".join(lines[1:])
        text_part, _, sources_part = body.partition("Sources:")
        sources = [
            ln.strip()[2:].strip() for ln in sources_part.splitlines() if ln.strip().startswith("- ")
        ]
        blocks[slug] = {"name": name, "text": text_part.strip(), "sources": sources}
    return blocks


def build_entry(
    slug: str, block: dict, model_hashes: dict, timestamp: str, frame: str = FRAME, arm: str = "B"
) -> dict:
    species_url = next(
        (s for s in block["sources"] if s.startswith("https://www.dndbeyond.com/species/")), None
    )
    if species_url is None:
        print(f"block {slug} has no species URL in its Sources", file=sys.stderr)
        sys.exit(2)
    entry = {
        "character": slug,
        "arm": arm,
        "prompt": f"{frame} {ADDENDUM} {block['text']}",
        "frame": frame,
        "species_sources": {species_url.rsplit("/", 1)[-1]: species_url},
        "seed": SEED,
        "model_hashes": model_hashes,
        "workflow": WORKFLOW,
        "output": None,
        "timestamp": timestamp,
    }
    assert list(entry.keys()) == PROMPT_KEYS
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptions", required=True, help="authored descriptions.md")
    parser.add_argument("--out-dir", required=True, help="arm_b output dir")
    parser.add_argument("--model-path", required=True, help="local flux3 unet file to hash")
    parser.add_argument("--frame", default=FRAME, help="frame sentence (default = Arm B frame)")
    parser.add_argument("--arm", default="B", help='arm label for prompts.json (default "B")')
    args = parser.parse_args()

    blocks = parse_descriptions(args.descriptions)
    if set(blocks) != set(SLUGS):
        print(f"expected slugs {sorted(SLUGS)}, found {sorted(blocks)}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.model_path):
        print(f"model file missing: {args.model_path}", file=sys.stderr)
        sys.exit(2)

    model_hashes = {"unet_name": UNet_NAME, "sha256": sha256_of(args.model_path)}
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entries = {
        slug: build_entry(slug, blocks[slug], model_hashes, timestamp, frame=args.frame, arm=args.arm)
        for slug in sorted(blocks)
    }

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, "prompts.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(entries)} Arm B prompts to {out_path}")


if __name__ == "__main__":
    main()
