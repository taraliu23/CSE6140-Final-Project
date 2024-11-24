from itertools import permutations
import time
from utils import create_distance_matrix


def brute_force_tsp(points, cutoff):
    """
    Finds the TSP tour using brute force within the time cutoff.
    :param points: List of (id, x, y) tuples.
    :param cutoff: Time limit in seconds.
    :return: (cost, tour) where cost is the total distance and tour is the list of indices.
    """
    start_time = time.time()

    # Validate input
    if not points or len(points) == 0:
        raise ValueError("No points provided for TSP")

    best_cost = float('inf')
    best_tour = []
    n = len(points)
    distance_matrix = create_distance_matrix(points)

    # Iterate through all permutations
    for perm in permutations(range(n)):
        if time.time() - start_time > cutoff:
            break
        cost = sum(distance_matrix[perm[i]][perm[i + 1]] for i in range(n - 1))
        cost += distance_matrix[perm[-1]][perm[0]]  # Complete the cycle
        if cost < best_cost:
            best_cost = cost
            best_tour = perm

    return best_cost, list(best_tour)
