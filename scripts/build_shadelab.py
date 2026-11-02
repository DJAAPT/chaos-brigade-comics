"""Build the Shade-lab prompt set: one revised block, four seeds.

Reads the lab's single authored shade block and emits shade-lab/workspace
prompts.json entries shade_s0..shade_s3 with the lab seed ladder
(424242 control, 424243 re-roll, 777001 and 314159 independent), Arm C
framing, arm label "C". Reuses the Arm-B builder's constants so the
frame/addendum/keys stay single-sourced.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    from scripts.build_arm_b import (
        ADDENDUM,
        FRAME_C,
        PROMPT_KEYS,
        UNet_NAME,
        WORKFLOW,
        parse_descriptions,
        sha256_of,
    )
except ImportError:  # run as a plain script from the repo root
    from build_arm_b import (  # type: ignore
        ADDENDUM,
        FRAME_C,
        PROMPT_KEYS,
        UNet_NAME,
        WORKFLOW,
        parse_descriptions,
        sha256_of,
    )

SEEDS = (424242, 424243, 777001, 314159)
KEYS = tuple(f"shade_s{i}" for i in range(len(SEEDS)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptions", required=True, help="lab descriptions.md with one shade block")
    parser.add_argument("--out-dir", required=True, help="shade-lab output dir")
    parser.add_argument("--model-path", required=True, help="local flux3 unet file to hash")
    parser.add_argument(
        "--seeds", type=int, nargs="+", default=None,
        help="seed ladder (default: the original four-seed ladder)",
    )
    parser.add_argument(
        "--keys", nargs="+", default=None,
        help="entry keys matching --seeds (default: shade_s0..)",
    )
    args = parser.parse_args()

    seeds = tuple(args.seeds) if args.seeds is not None else SEEDS
    keys = tuple(args.keys) if args.keys is not None else tuple(f"shade_s{i}" for i in range(len(seeds)))
    if len(keys) != len(seeds):
        print(f"--keys ({len(keys)}) and --seeds ({len(seeds)}) must match in length", file=sys.stderr)
        sys.exit(2)
    if len(set(keys)) != len(keys):
        print(f"--keys must be unique, got {list(keys)}", file=sys.stderr)
        sys.exit(2)

    blocks = parse_descriptions(args.descriptions)
    if set(blocks) != {"shade"}:
        print(f"expected exactly the shade block, found {sorted(blocks)}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.model_path):
        print(f"model file missing: {args.model_path}", file=sys.stderr)
        sys.exit(2)

    block = blocks["shade"]
    species_url = next(
        (s for s in block["sources"] if s.startswith("https://www.dndbeyond.com/species/")), None
    )
    if species_url is None:
        print("shade block has no species URL in its Sources", file=sys.stderr)
        sys.exit(2)

    model_hashes = {"unet_name": UNet_NAME, "sha256": sha256_of(args.model_path)}
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    prompt = f"{FRAME_C} {ADDENDUM} {block['text']}"

    entries = {}
    for key, seed in zip(keys, seeds):
        entry = {
            "character": key,
            "arm": "C",
            "prompt": prompt,
            "frame": FRAME_C,
            "species_sources": {species_url.rsplit("/", 1)[-1]: species_url},
            "seed": seed,
            "model_hashes": model_hashes,
            "workflow": "workflows/base_flux3.json",
            "output": None,
            "timestamp": timestamp,
        }
        assert list(entry.keys()) == PROMPT_KEYS
        entries[key] = entry

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, "prompts.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(entries)} Shade-lab prompts to {out_path}")


if __name__ == "__main__":
    main()
