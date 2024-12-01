# mst_approximation.py
from scipy.sparse.csgraph import minimum_spanning_tree
from utils import create_distance_matrix


def mst_approximation_tsp(points):
    """Approximates TSP using a Minimum Spanning Tree."""
    distance_matrix = create_distance_matrix(points)
    mst = minimum_spanning_tree(distance_matrix).toarray()
    visited = set()

    def dfs(node, tour):
        visited.add(node)
        tour.append(node)
        for neighbor in range(len(points)):
            if mst[node][neighbor] > 0 and neighbor not in visited:
                dfs(neighbor, tour)

    tour = []
    dfs(0, tour)
    tour.append(0)

    cost = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))
    return cost, tour
