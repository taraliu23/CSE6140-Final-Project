# simulated_annealing.py
# Author: Tingyu 'Tara' Liu
# Date: 2024-11-27

# This is the implementation of the Simulated Annealing algorithm for the Traveling Salesman Problem (TSP).
# The function simulated_annealing_tsp takes a list of points and a cutoff time, and returns the best tour found
# within the time limit. The points are given as a list of (id, x, y) tuples, where id is an integer identifier
# and x, y are the coordinates. The cutoff time is given in seconds. The function returns a tuple (cost, tour)
# where cost is the total distance of the tour and tour is a list of indices representing the order of the cities visited.
# The function uses a random seed for reproducibility.

# The algorithm works as follows:
# 1. Initialize with a random tour.
# 2. Define the annealing parameters: initial temperature, cooling rate, and minimum temperature.
# 3. Generate a neighbor by swapping two cities in the current tour.
# 4. Accept the new tour based on the acceptance probability.
# 5. Cool down the temperature and repeat until the minimum temperature is reached or the time limit is exceeded.

# The acceptance probability is calculated as exp((current_cost - new_cost) / T), where T is the current temperature.


# example usage:
# cost, tour = simulated_annealing_tsp(points, cutoff=1, seed=0)


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


def simulated_annealing_tsp(points, cutoff, seed=None):
    """Finds a near-optimal TSP tour using simulated annealing."""
    random.seed(seed)
    start_time = time.time()
    n = len(points)
    if n == 0:
        raise ValueError("No points provided for TSP")

    distance_matrix = create_distance_matrix(points)

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


def simulated_annealing_tsp(points, cutoff, seed=None):
    """
    Solves the TSP using Simulated Annealing.
    :param points: List of (id, x, y) tuples.
    :param cutoff: Time limit in seconds.
    :param seed: Random seed for reproducibility.
    :return: (cost, tour) where cost is the total distance and tour is the list of indices.
    """
    random.seed(seed)
    n = len(points)
    if n == 0:
        raise ValueError("No points provided for TSP")

    distance_matrix = create_distance_matrix(points)

    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = calculate_cost(current_tour, distance_matrix)

    best_tour = current_tour[:]
    best_cost = current_cost

    T = 1000  # Initial temperature
    alpha = 0.995  # Cooling rate
    epsilon = 1e-3  # Min temperature
    start_time = time.time()

    while T > epsilon and (time.time() - start_time) < cutoff:
        i, j = random.sample(range(n), 2)
        new_tour = current_tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        new_cost = calculate_cost(new_tour, distance_matrix)

        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / T):
            current_tour = new_tour
            current_cost = new_cost

            if new_cost < best_cost:
                best_tour = new_tour
                best_cost = new_cost

        T *= alpha

    return best_cost, best_tour
