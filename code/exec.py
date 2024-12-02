# exec.py
# Author: Tingyu 'Tara' Liu
# Date: 2024-11-27

# This is the main file that will be used to run the algorithms: BF, Approx, LS
# it takes in the command line arguments and run the according algorithm
# then save the results to a csv file and a log file
# functions: save_results_to_csv, calculate_relative_error, execute_algorithm, parse_args

# example usage:
# python exec.py -inst input/Atlanta.tsp -alg Approx -time 200 -seed 42
# python exec.py -inst input/Atlanta.tsp -alg BF -time 10 -seed 1
# python exec.py -inst input/Atlanta.tsp -alg LS -time 10 -seed 1


import os
from algorithms import brute_force, mst_approximation, simulated_annealing
from utils import read_tsp
import time
import sys
import csv


def save_results_to_csv(file_path, method, elapsed_time, cost, full_tour, rel_error):
    """
    Appends performance data to a CSV file.
    """
    output_csv = os.path.join(os.path.dirname(
        __file__), "output", "results.csv")
    is_new_file = not os.path.exists(output_csv)

    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow(["Dataset", "Algorithm", "Time(s)",
                            "Solution Quality", "Full Tour", "RelError"])

        writer.writerow(
            [file_path, method, f"{elapsed_time:.2f}", f"{cost:.2f}", full_tour, f"{rel_error:.2%}"])


def calculate_relative_error(current_cost, best_cost):
    """
    Calculates the relative error compared to the best-known cost.
    """
    return (current_cost - best_cost) / best_cost if best_cost > 0 else 0.0


def execute_algorithm(file_path, method, cutoff, seed=None, best_cost=None):
    """Executes a specific TSP solving method."""
    points = read_tsp(file_path)

    if not points or len(points) == 0:
        raise ValueError(f"TSP file {file_path} does not contain valid data")

    name = os.path.basename(file_path).split('.')[0]

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir, f"{name}_{method}_{str(cutoff)}{f'_{seed}' if seed else ''}.sol")

    log_file = os.path.join(output_dir, "timing_log.txt")

    start_time = time.time()

    if method == "BF":  # Brute Force
        print('algorithm: Brute Force')
        brute_force.brute_force_tsp(points, cutoff)
        cost, tour = brute_force.brute_force_tsp(points, cutoff)
    elif method == "Approx":  # 2-Approximation with MST
        print('algorithm: 2-Approximation with MST')
        cost, tour = mst_approximation.mst_approximation_tsp(points)
    elif method == "LS":  # Local Search with Simulated Annealing
        if seed is None:
            raise ValueError("Seed is required for Local Search")
        print('algorithm: Local Search with Simulated Annealing')
        cost, tour = simulated_annealing.simulated_annealing_tsp(
            points, cutoff, seed)
    else:
        raise ValueError(f"Unknown method: {method}")

    end_time = time.time()
    elapsed_time = end_time - start_time

    full_tour = "Yes" if len(set(tour)) == len(points) else "No"
    rel_error = calculate_relative_error(cost, best_cost) if best_cost else 0.0

    save_results_to_csv(name, method, elapsed_time, cost, full_tour, rel_error)

    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(",".join(map(str, [points[i][0] for i in tour])))

    with open(log_file, 'a') as log:
        log.write(f"{name} - {method}: {elapsed_time:.2f} seconds\n")

    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(",".join(map(str, [points[i][0] for i in tour])))

    print(f"Cost: {cost:.2f}")
    print(f"Tour: {tour}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Full tour: {full_tour}")
    print(f"Relative error: {rel_error:.2%}")
    # print(f"Results saved to {output_file}")
    print(
        f"Results saved to output/{name}_{method}_{str(cutoff)}{f'_{seed}' if seed else ''}.sol")
    # print(f"Log saved to {log_file}")
    print(f"Log saved to output/timing_log.txt")


def parse_args(args):
    '''
    Parses command-line arguments
    params: args: list of command-line arguments
    returns: file_path: str, method: str, cutoff: int, seed: int
    '''

    if "-inst" not in args or "-alg" not in args or "-time" not in args:
        raise ValueError(
            "Usage: exec -inst <filename> -alg [BF | Approx | LS] -time <cutoff_in_seconds> [-seed <random_seed>]")

    file_path = args[args.index("-inst") + 1]
    method = args[args.index("-alg") + 1]
    cutoff = int(args[args.index("-time") + 1])

    seed = None
    if "-seed" in args:
        seed = int(args[args.index("-seed") + 1])

    return file_path, method, cutoff, seed


# Main function
if __name__ == "__main__":
    try:
        print('start exec...')
        # print('args:', sys.argv)
        file_path, method, cutoff, seed = parse_args(sys.argv)
        execute_algorithm(file_path, method, cutoff, seed)
        print('end exec...')

    except Exception as e:
        print(f"Error: {e}")
        print(
            "Usage: exec -inst <filename> -alg [BF | Approx | LS] -time <cutoff_in_seconds> [-seed <random_seed>]")
        sys.exit(1)
