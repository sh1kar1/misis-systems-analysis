import json

def main(rank_a_str, rank_b_str):
    rank_a = json.loads(rank_a_str)
    rank_b = json.loads(rank_b_str)
    
    objects = set()
    for item in rank_a:
        if isinstance(item, list):
            objects.update(item)
        else:
            objects.add(item)
    for item in rank_b:
        if isinstance(item, list):
            objects.update(item)
        else:
            objects.add(item)
    
    objects = sorted(list(objects))
    n = len(objects)
    obj_to_idx = {obj: i for i, obj in enumerate(objects)}
    
    def rank_to_matrix(rank):
        matrix = [[0] * n for _ in range(n)]
        for i in range(len(rank)):
            cluster_i = rank[i] if isinstance(rank[i], list) else [rank[i]]
            for obj_i in cluster_i:
                idx_i = obj_to_idx[obj_i]
                for j in range(i, len(rank)):
                    cluster_j = rank[j] if isinstance(rank[j], list) else [rank[j]]
                    for obj_j in cluster_j:
                        idx_j = obj_to_idx[obj_j]
                        matrix[idx_i][idx_j] = 1
        return matrix
    
    def transpose(matrix):
        return [[matrix[j][i] for j in range(n)] for i in range(n)]
    
    def logical_and(m1, m2):
        return [[m1[i][j] & m2[i][j] for j in range(n)] for i in range(n)]
    
    def logical_or(m1, m2):
        return [[m1[i][j] | m2[i][j] for j in range(n)] for i in range(n)]
    
    YA = rank_to_matrix(rank_a)
    YB = rank_to_matrix(rank_b)
    YA_T = transpose(YA)
    YB_T = transpose(YB)
    
    P = logical_or(logical_and(YA, YB_T), logical_and(YA_T, YB))
    
    contradictions = []
    for i in range(n):
        for j in range(i + 1, n):
            if YA[i][j] == 1 and YA[j][i] == 0 and YB[i][j] == 0 and YB[j][i] == 1:
                contradictions.append([objects[i], objects[j]])
            elif YA[i][j] == 0 and YA[j][i] == 1 and YB[i][j] == 1 and YB[j][i] == 0:
                contradictions.append([objects[i], objects[j]])
    
    C = logical_and(YA, YB)
    
    for pair in contradictions:
        i = obj_to_idx[pair[0]]
        j = obj_to_idx[pair[1]]
        C[i][j] = 1
        C[j][i] = 1
    
    E = logical_and(C, transpose(C))
    
    def warshall(matrix):
        m = [row[:] for row in matrix]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    m[i][j] = m[i][j] | (m[i][k] & m[k][j])
        return m
    
    E_star = warshall(E)
    
    visited = [False] * n
    clusters = []
    for i in range(n):
        if not visited[i]:
            cluster = []
            for j in range(n):
                if E_star[i][j] == 1:
                    cluster.append(objects[j])
                    visited[j] = True
            clusters.append(sorted(cluster))
    
    def cluster_less_than(c1, c2):
        for obj1 in c1:
            for obj2 in c2:
                i1 = obj_to_idx[obj1]
                i2 = obj_to_idx[obj2]
                if C[i1][i2] == 1 and C[i2][i1] == 0:
                    return True
        return False
    
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            if cluster_less_than(clusters[j], clusters[i]):
                clusters[i], clusters[j] = clusters[j], clusters[i]
    
    result = []
    for cluster in clusters:
        if len(cluster) == 1:
            result.append(cluster[0])
        else:
            result.append(cluster)
    
    return json.dumps({
        "contradictions": contradictions,
        "consensus_ranking": result
    })
