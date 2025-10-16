from argparse import ArgumentParser
from pathlib import Path
from typing import List


def main(s: str) -> List[List[bool]]:
    edges = []
    nodes = set()
    for line in s.strip().split("\\n"):
        u, v = line.split(",")
        edges.append((u, v))
        nodes.update([u, v])

    nodes_list = sorted(nodes)
    node_to_idx = {node: idx for idx, node in enumerate(nodes_list)}
    n = len(nodes_list)

    adjacency_matrix = [[False] * n for _ in range(n)]

    for u, v in edges:
        i, j = node_to_idx[u], node_to_idx[v]
        adjacency_matrix[i][j] = True

    return adjacency_matrix


if __name__ == "__main__":
    parser = ArgumentParser(description="Build adjacency matrix from CSV edges")
    parser.add_argument("s", type=str, help="CSV string with edges")
    args = parser.parse_args()

    result = main(args.s)

    for row in result:
        print([int(x) for x in row])
