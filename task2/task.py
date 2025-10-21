from argparse import ArgumentParser
from collections import deque
from pathlib import Path
import math
from typing import Tuple


def main(s: str, e: str) -> Tuple[float, float]:
    path = Path(s)
    if path.exists() and path.is_file():
        with open(path, "r") as f:
            data = f.read().strip()
    else:
        data = s.strip()

    edges = []
    nodes = set()
    lines = data.replace('\\n', '\n').split('\n')
    for line in lines:
        if line.strip():
            u, v = line.strip().split(",")
            edges.append((u.strip(), v.strip()))
            nodes.update([u.strip(), v.strip()])

    nodes.add(e.strip())
    nodes_list = sorted(nodes)
    node_to_idx = {node: idx for idx, node in enumerate(nodes_list)}
    n = len(nodes_list)

    adjacency = [[0] * n for _ in range(n)]
    for u, v in edges:
        i, j = node_to_idx[u], node_to_idx[v]
        adjacency[i][j] = 1

    reachability = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            reachability[i][j] = adjacency[i][j]
        reachability[i][i] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if not reachability[i][j]:
                    reachability[i][j] = reachability[i][k] and reachability[k][j]

    reachable_counts = [sum(row) for row in reachability]
    total_reachable = sum(reachable_counts)

    if total_reachable > 0:
        p_reach = [count / total_reachable for count in reachable_counts]
        entropy = 0.0
        for p in p_reach:
            if p > 0:
                entropy -= p * math.log2(p)
    else:
        entropy = 0.0

    root_idx = node_to_idx[e]
    visited = [False] * n
    depth = [0] * n
    children_count = [0] * n

    queue = deque([root_idx])
    visited[root_idx] = True

    while queue:
        current = queue.popleft()
        for neighbor in range(n):
            if adjacency[current][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                depth[neighbor] = depth[current] + 1
                children_count[current] += 1
                queue.append(neighbor)

    max_depth = max(depth) if depth else 0
    avg_children = sum(children_count) / n if n > 0 else 0

    max_entropy = math.log2(n) if n > 0 else 1
    norm_entropy = entropy / max_entropy if max_entropy > 0 else 0
    norm_depth = max_depth / (n - 1) if n > 1 else 0
    norm_branching = avg_children / (n - 1) if n > 1 else 0

    structural_complexity = 0.5 * norm_entropy + 0.3 * norm_depth + 0.2 * norm_branching
    norm_complexity = structural_complexity * 10

    entropy_rounded = round(entropy, 1)
    complexity_rounded = round(norm_complexity, 1)

    return (entropy_rounded, complexity_rounded)


if __name__ == "__main__":
    parser = ArgumentParser(description="Calculate graph entropy and structural complexity")
    parser.add_argument("s", type=str, help="CSV string or path to CSV file")
    parser.add_argument("e", type=str, help="Root node identifier")
    args = parser.parse_args()

    entropy, complexity = main(args.s, args.e)
    print(f"({entropy}, {complexity})")
