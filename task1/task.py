from argparse import ArgumentParser
from pathlib import Path
from typing import List, Tuple

import numpy as np


def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    path = Path(s)
    if path.exists() and path.is_file():
        with open(path, "r") as f:
            data = f.read().strip()
    else:
        data = s.strip()

    edges = []
    nodes = set()
    for line in data.split("\\n"):
        u, v = line.strip().split(",")
        edges.append((u, v))
        nodes.update([u, v])

    nodes.add(e)

    nodes_list = sorted(nodes)
    node_to_idx = {node: idx for idx, node in enumerate(nodes_list)}
    n = len(nodes_list)

    r1 = np.zeros((n, n), dtype=bool)
    r2 = np.zeros((n, n), dtype=bool)
    r3 = np.zeros((n, n), dtype=bool)
    r4 = np.zeros((n, n), dtype=bool)
    r5 = np.zeros((n, n), dtype=bool)

    for u, v in edges:
        i, j = node_to_idx[u], node_to_idx[v]
        r1[i, j] = True
        r2[j, i] = True

    closure = r1.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i, j] = closure[i, j] or (closure[i, k] and closure[k, j])
    r3 = closure

    r4 = r3.T

    from collections import defaultdict
    parent_children = defaultdict(list)
    for u, v in edges:
        parent_children[u].append(v)

    for parent, children in parent_children.items():
        if len(children) > 1:
            indices = [node_to_idx[child] for child in children]
            for i in indices:
                for j in indices:
                    if i != j:
                        r5[i, j] = True

    return (
        r1.tolist(),
        r2.tolist(),
        r3.tolist(),
        r4.tolist(),
        r5.tolist()
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="Process tree relations")
    parser.add_argument("s", type=str, help="CSV string or path to CSV file")
    parser.add_argument("e", type=str, help="Root node identifier")
    args = parser.parse_args()

    result = main(args.s, args.e)
    relations = ["r1", "r2", "r3", "r4", "r5"]
    for rel, matrix in zip(relations, result):
        print(f"{rel}:")
        for row in matrix:
            print([int(x) for x in row])
        print()
