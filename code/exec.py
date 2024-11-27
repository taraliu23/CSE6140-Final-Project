# exec.py
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
        # Write the header if this is a new CSV file
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

    cutoff = 200  # Hard-coded cutoff time
    name = os.path.basename(file_path).split('.')[0]

    # Ensure the output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Construct output file path
    output_file = os.path.join(
        output_dir, f"{name}_{method}_{cutoff}{f'_{seed}' if seed else ''}.sol")

    # Log file for execution times
    log_file = os.path.join(output_dir, "timing_log.txt")

    # Start measuring time
    start_time = time.time()

    if method == "BF":  # Brute Force
        cost, tour = brute_force.brute_force_tsp(points, cutoff)
    elif method == "Approx":  # MST Approximation
        cost, tour = mst_approximation.mst_approximation_tsp(points)
    elif method == "LS":  # Local Search (Simulated Annealing)
        if seed is None:
            raise ValueError("Seed is required for Local Search")
        cost, tour = simulated_annealing.simulated_annealing_tsp(
            points, cutoff, seed)
    else:
        raise ValueError(f"Unknown method: {method}")

    # Stop measuring time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Determine if a full tour was completed
    full_tour = "Yes" if len(set(tour)) == len(points) else "No"

    # Calculate relative error
    rel_error = calculate_relative_error(cost, best_cost) if best_cost else 0.0

    # Save results to CSV
    save_results_to_csv(name, method, elapsed_time, cost, full_tour, rel_error)

    # Write results to the output file
    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(",".join(map(str, [points[i][0] for i in tour])))

        # Log the timing results
    with open(log_file, 'a') as log:
        log.write(f"{name} - {method}: {elapsed_time:.2f} seconds\n")

        # Write results to the output file
    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(",".join(map(str, [points[i][0] for i in tour])))


def parse_args(args):
    """Parses command-line arguments."""
    if "-inst" not in args or "-alg" not in args or "-time" not in args:
        raise ValueError(
            "Usage: exec -inst <filename> -alg [BF | Approx | LS] -time <cutoff_in_seconds> [-seed <random_seed>]")

    # Extract required arguments
    file_path = args[args.index("-inst") + 1]
    method = args[args.index("-alg") + 1]
    cutoff = int(args[args.index("-time") + 1])

    # Extract optional arguments
    seed = None
    if "-seed" in args:
        seed = int(args[args.index("-seed") + 1])

    return file_path, method, cutoff, seed


if __name__ == "__main__":

    # if len(sys.argv) < 3 or len(sys.argv) > 4:
    #     print("Usage: python exec.py <filename> <method> [<seed>]")
    #     sys.exit(1)

    # file_path = sys.argv[1]
    # method = sys.argv[2]
    # seed = int(sys.argv[3]) if len(sys.argv) == 4 else None

    # execute_algorithm(file_path, method, seed)

    try:
        # Parse command-line arguments
        file_path, method, cutoff, seed = parse_args(sys.argv)
        execute_algorithm(file_path, method, cutoff, seed)
    except Exception as e:
        print(f"Error: {e}")
        print(
            "Usage: exec -inst <filename> -alg [BF | Approx | LS] -time <cutoff_in_seconds> [-seed <random_seed>]")
        sys.exit(1)
