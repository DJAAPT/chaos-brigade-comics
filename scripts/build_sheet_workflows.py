"""Generate per-character Flux3 workflow JSONs for the sheet-test.

Deep-copies the pinned base graph once per character, swaps the
{{PROMPT}} sentinel for that character's Arm A prompt, pins every
seed/noise_seed input to 424242, and points SaveImage at a
per-character filename prefix. Nothing else in the graph changes.
"""
import argparse
import copy
import json
import os
import sys

SEED = 424242
SENTINEL = "{{PROMPT}}"


def build_one(base, prompt, slug, prefix="sheettest_", seed=None):
    if seed is None:
        seed = SEED
    graph = copy.deepcopy(base)

    prompt_nodes = [
        node_id
        for node_id, node in graph.items()
        if node.get("inputs", {}).get("text") == SENTINEL
    ]
    if len(prompt_nodes) != 1:
        print(f"expected exactly one {SENTINEL} node, found {len(prompt_nodes)}: {prompt_nodes}", file=sys.stderr)
        sys.exit(2)
    graph[prompt_nodes[0]]["inputs"]["text"] = prompt

    save_nodes = [node_id for node_id, node in graph.items() if node["class_type"] == "SaveImage"]
    if len(save_nodes) != 1:
        print(f"expected exactly one SaveImage node, found {len(save_nodes)}", file=sys.stderr)
        sys.exit(2)
    graph[save_nodes[0]]["inputs"]["filename_prefix"] = f"{prefix}{slug}"

    for node in graph.values():
        inputs = node.get("inputs", {})
        for key in ("seed", "noise_seed"):
            if key in inputs:
                inputs[key] = seed
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="pinned base workflow JSON")
    parser.add_argument("--prompts", required=True, help="prompts.json from the sheet bible build")
    parser.add_argument("--out-dir", required=True, help="directory for per-character workflows")
    parser.add_argument("--prefix", default="sheettest_", help="output filename/SaveImage prefix (round-1 default)")
    args = parser.parse_args()

    with open(args.base, encoding="utf-8") as f:
        base = json.load(f)
    with open(args.prompts, encoding="utf-8") as f:
        prompts = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True)
    for slug in sorted(prompts):
        graph = build_one(base, prompts[slug]["prompt"], slug, prefix=args.prefix, seed=prompts[slug].get("seed", SEED))
        out_path = os.path.join(args.out_dir, f"{args.prefix}{slug}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
