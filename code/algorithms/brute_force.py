from itertools import permutations
import time
from utils import create_distance_matrix

# brute_force_tsp function


def brute_force_tsp(v, cutoff):
    """
    Finds the TSP tour using brute force within the time cutoff.
    :param v: List of (id, x, y) tuples.
    :param cutoff: Time limit in seconds.
    :return: (cost, tour) where cost is the total distance and tour is the list of indices.
    """
    start_time = time.time()

    if not v or len(v) == 0:
        raise ValueError("No v provided for TSP")

    best_cost = float('inf')
    best_tour = []
    n = len(v)
    distance_matrix = create_distance_matrix(v)

    for i in permutations(range(n)):
        if time.time() - start_time > cutoff:
            break
        cost = sum(distance_matrix[i[i]][i[i + 1]] for i in range(n - 1))
        cost += distance_matrix[i[-1]][i[0]]  # Complete the cycle
        if cost < best_cost:
            best_cost = cost
            best_tour = i

    return best_cost, list(best_tour)
