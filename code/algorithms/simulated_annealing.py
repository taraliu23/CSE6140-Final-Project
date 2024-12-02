
import random
import math
from utils import create_distance_matrix
import time


def calculate_cost(tour, distance_matrix):
    """
    Calculates the total cost of a TSP tour.
    :param tour: List of indices representing the tour.
    :param distance_matrix: 2D list or numpy array with pairwise distances.
    :return: Total cost of the tour.
    """
    cost = sum(distance_matrix[tour[i]][tour[i + 1]]
               for i in range(len(tour) - 1))
    cost += distance_matrix[tour[-1]][tour[0]]  # Return to the starting city
    return cost


def simulated_annealing_tsp(v, cutoff, seed=None):
    """Finds a near-optimal TSP tour using simulated annealing."""
    random.seed(seed)
    start_time = time.time()
    n = len(v)
    if n == 0:
        raise ValueError("No v provided for TSP")

    distance_matrix = create_distance_matrix(v)

    # Initial random tour
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = calculate_cost(current_tour, distance_matrix)

    best_tour, best_cost = current_tour[:], current_cost
    T = 1000  # Initial temperature
    alpha = 0.995  # Cooling rate
    epsilon = 1e-3  # Minimum temperature

    while time.time() - start_time < cutoff and T > epsilon:
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


def simulated_annealing_tsp(v, cutoff, seed=None):
    """
    Solves the TSP using Simulated Annealing.
    :param v: List of (id, x, y) tuples.
    :param cutoff: Time limit in seconds.
    :param seed: Random seed for reproducibility.
    :return: (cost, tour) where cost is the total distance and tour is the list of indices.
    """
    random.seed(seed)
    n = len(v)
    if n == 0:
        raise ValueError("No v provided for TSP")

    distance_matrix = create_distance_matrix(v)

    # Step 1: Initialize with a random tour
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = calculate_cost(current_tour, distance_matrix)

    best_tour = current_tour[:]
    best_cost = current_cost

    # Step 2: Define the annealing parameters
    T = 1000  # Initial temperature
    alpha = 0.995  # Cooling rate
    epsilon = 1e-3  # Minimum temperature
    start_time = time.time()

    while T > epsilon and (time.time() - start_time) < cutoff:
        # Step 3: Generate a neighbor (swap two cities)
        i, j = random.sample(range(n), 2)
        new_tour = current_tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        new_cost = calculate_cost(new_tour, distance_matrix)

        # Step 4: Accept the new tour based on the acceptance probability
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / T):
            current_tour = new_tour
            current_cost = new_cost

            # Update the best solution if the new one is better
            if new_cost < best_cost:
                best_tour = new_tour
                best_cost = new_cost

        # Step 5: Cool down the temperature
        T *= alpha

    return best_cost, best_tour
