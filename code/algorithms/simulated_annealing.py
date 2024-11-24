# simulated_annealing.py
import random
import math


def simulated_annealing_tsp(points, cutoff, seed=None):
    """Finds a near-optimal TSP tour using simulated annealing."""
    random.seed(seed)
    start_time = time.time()
    n = len(points)
    distance_matrix = create_distance_matrix(points)

    # Initial random tour
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = calculate_cost(current_tour, distance_matrix)

    best_tour, best_cost = current_tour[:], current_cost
    T = 1000  # Initial temperature
    alpha = 0.995  # Cooling rate

    while time.time() - start_time < cutoff and T > 1e-3:
        # Swap two cities
        i, j = random.sample(range(n), 2)
        new_tour = current_tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        new_cost = calculate_cost(new_tour, distance_matrix)

        # Accept the new tour based on probability
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / T):
            current_tour, current_cost = new_tour, new_cost

        # Update the best solution
        if current_cost < best_cost:
            best_tour, best_cost = current_tour[:], current_cost

        T *= alpha  # Cool down

    return best_cost, best_tour
