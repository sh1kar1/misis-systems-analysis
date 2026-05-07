from typing import List, Tuple

def _parse_edges(csv_text: str) -> List[List[str]]:
    if not csv_text:
        return []
    
    lines = [ln.strip() for ln in csv_text.replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    non_empty_lines = [ln for ln in lines if ln != '']

    edges = []
    
    if len(non_empty_lines) == 1:
        items = [t.strip() for t in non_empty_lines[0].split(',') if t.strip() != '']
        for i in range(0, len(items) - 1, 2):
            edges.append([items[i], items[i + 1]])
    else:
        for ln in non_empty_lines:
            parts = [t.strip() for t in ln.split(',')]
            if len(parts) >= 2:
                edges.append([parts[0], parts[1]])
                
    return edges

def _sort_vertices(vertices_set: set) -> List[str]:
    try:
        return sorted(list(vertices_set), key=int)
    except ValueError:
        return sorted(list(vertices_set))

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    edges = _parse_edges(s)

    vertices_set = set()
    for u, v in edges:
        vertices_set.add(u)
        vertices_set.add(v)

    vertices_set.add(e)

    vertices = _sort_vertices(vertices_set)
    n = len(vertices)
    
    if n == 0:
        return [], [], [], [], []

    index_by_vertex = {v: i for i, v in enumerate(vertices)}

    adj = [[False] * n for _ in range(n)]
    children = [[] for _ in range(n)]
    parent = [-1] * n

    for u, v in edges:
        ui = index_by_vertex[u]
        vi = index_by_vertex[v]
        adj[ui][vi] = True
        children[ui].append(vi)
        parent[vi] = ui

    r1 = [[adj[i][j] for j in range(n)] for i in range(n)]

    r2 = [[r1[j][i] for j in range(n)] for i in range(n)]

    descendants = [set() for _ in range(n)]

    def dfs(start: int, current: int):
        for child in children[current]:
            descendants[start].add(child)
            dfs(start, child)

    for i in range(n):
        dfs(i, i)

    r3 = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in descendants[i]:
            if not adj[i][j]:
                r3[i][j] = True

    r4 = [[r3[j][i] for j in range(n)] for i in range(n)]

    r5 = [[False] * n for _ in range(n)]
    siblings_by_parent = [[] for _ in range(n)]
    
    for node_idx in range(n):
        p = parent[node_idx]
        if p != -1:
            siblings_by_parent[p].append(node_idx)
            
    for sibs in siblings_by_parent:
        if len(sibs) >= 2:
            for i in sibs:
                for j in sibs:
                    if i != j:
                        r5[i][j] = True

    return r1, r2, r3, r4, r5

if __name__ == "__main__":
    test_str = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
    root = "1"
    matrices = main(test_str, root)
    
    for idx, matrix in enumerate(matrices, 1):
        print(f"Матрица R{idx}:")
        for row in matrix:
            print([int(val) for val in row])
        print()
