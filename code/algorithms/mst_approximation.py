# mst_approximation.py
# Author: Tingyu 'Tara' Liu
# Date: 2024-11-27

# This is the Minimum Spanning Tree approximation algorithm that will be used to solve the TSP problem
# it takes in the points and return the best cost and the best tour
# functions: mst_approximation_tsp

# example usage:
# mst_approximation_tsp(points)
# mst_approximation_tsp([(0, 38, 43), (1, 39, 40), (2, 39, 42)])

from scipy.sparse.csgraph import minimum_spanning_tree
from utils import create_distance_matrix

# minimum_spanning_tree(csgraph, overwrite=False)
# Return a minimum spanning tree of an undirected graph

# A minimum spanning tree is a graph consisting of the subset of edges which together connect all connected nodes, while minimizing the total sum of weights on the edges.
# This is computed using the Kruskal algorithm.
#  input graph             minimum spanning tree

#      (0)                         (0)
#     /   \                       /
#    3     8                     3
#   /       \                   /
# (3)---5---(1)               (3)---5---(1)
#   \       /                           /
#    6     2                           2
#     \   /                           /
#      (2)                         (2)


def mst_approximation_tsp(points):
    """Approximates TSP using a Minimum Spanning Tree.
    params: points: List of (id, x, y) tuples.
    return: (cost, tour) where cost is the total distance and tour is the list
    of indices
    """
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
