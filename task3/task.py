import json
from argparse import ArgumentParser
from typing import Dict, List, Tuple, Set


def main(s1: str, s2: str) -> str:
    rank1 = json.loads(s1)
    rank2 = json.loads(s2)

    all_elements = set()
    for cluster in rank1:
        all_elements.update(cluster)
    for cluster in rank2:
        all_elements.update(cluster)

    element_to_index = {elem: idx for idx, elem in enumerate(sorted(all_elements))}
    n = len(all_elements)

    matrix1 = [[0] * n for _ in range(n)]
    matrix2 = [[0] * n for _ in range(n)]

    for cluster in rank1:
        elements_in_cluster = list(cluster)
        for i in range(len(elements_in_cluster)):
            for j in range(len(elements_in_cluster)):
                idx_i = element_to_index[elements_in_cluster[i]]
                idx_j = element_to_index[elements_in_cluster[j]]
                matrix1[idx_i][idx_j] = 1

    for cluster in rank2:
        elements_in_cluster = list(cluster)
        for i in range(len(elements_in_cluster)):
            for j in range(len(elements_in_cluster)):
                idx_i = element_to_index[elements_in_cluster[i]]
                idx_j = element_to_index[elements_in_cluster[j]]
                matrix2[idx_i][idx_j] = 1

    conflict_core = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix1[i][j] != matrix2[i][j]:
                element_i = [k for k, v in element_to_index.items() if v == i][0]
                element_j = [k for k, v in element_to_index.items() if v == j][0]
                conflict_core.append([element_i, element_j])

    agreement_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix1[i][j] == 1 and matrix2[i][j] == 1:
                agreement_matrix[i][j] = 1

    visited = [False] * n
    clusters = []

    for i in range(n):
        if not visited[i]:
            current_cluster = set()
            stack = [i]

            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    element = [k for k, v in element_to_index.items() if v == node][0]
                    current_cluster.add(element)

                    for neighbor in range(n):
                        if agreement_matrix[node][neighbor] == 1 and not visited[neighbor]:
                            stack.append(neighbor)

            if current_cluster:
                clusters.append(sorted(list(current_cluster)))

    clusters.sort(key=lambda x: (-len(x), x[0]))

    return json.dumps(clusters, ensure_ascii=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Cluster ranking agreement")
    parser.add_argument("s1", type=str, help="First ranking JSON string")
    parser.add_argument("s2", type=str, help="Second ranking JSON string")
    args = parser.parse_args()

    result = main(args.s1, args.s2)
    print(result)
