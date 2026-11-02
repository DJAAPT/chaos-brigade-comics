"""Record one generated image into prompts.json (in-place audit update)."""
import argparse
import json


def record_output(prompts: dict, slug: str, output: str, timestamp: str) -> dict:
    """Set output/timestamp for one character's entry; KeyError on unknown slug."""
    if slug not in prompts:
        raise KeyError(f"unknown character: {slug}")
    prompts[slug]["output"] = output
    prompts[slug]["timestamp"] = timestamp
    return prompts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--character", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--timestamp", required=True)
    args = parser.parse_args()

    with open(args.prompts, encoding="utf-8") as f:
        prompts = json.load(f)
    record_output(prompts, args.character, args.output, args.timestamp)
    with open(args.prompts, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"recorded {args.character} -> {args.output}")


if __name__ == "__main__":
    main()
