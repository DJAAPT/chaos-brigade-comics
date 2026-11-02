"""Pin the Flux3 Klein base workflow for the sheet-test experiment.

Copies the in-repo bibleref graph to base_flux3.json with the single
populated CLIPTextEncode text node replaced by the {{PROMPT}} sentinel.
Everything else (loaders, sampler, steps, resolution) stays identical.
"""
import argparse
import json
import sys


def prepare(src_path: str, out_path: str) -> str:
    """Write base graph with its one populated text node set to the sentinel.

    Returns the id of the changed node. Exits 2 when the source has
    zero or multiple populated text nodes (wrong or drifted graph).
    """
    with open(src_path, encoding="utf-8") as f:
        graph = json.load(f)

    populated = [
        node_id
        for node_id, node in graph.items()
        if isinstance(node.get("inputs", {}).get("text"), str) and node["inputs"]["text"].strip()
    ]
    if len(populated) != 1:
        print(
            f"expected exactly one populated text node in {src_path}, "
            f"found {len(populated)}: {populated}",
            file=sys.stderr,
        )
        sys.exit(2)

    node_id = populated[0]
    graph[node_id]["inputs"]["text"] = "{{PROMPT}}"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"pinned {out_path}: node {node_id} text -> {{{{PROMPT}}}}")
    return node_id


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", required=True, help="source workflow JSON")
    parser.add_argument("--out", required=True, help="output base workflow JSON")
    args = parser.parse_args()
    prepare(args.src, args.out)


if __name__ == "__main__":
    main()
