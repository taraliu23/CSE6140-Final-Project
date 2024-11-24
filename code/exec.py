# exec.py
import os
from algorithms import brute_force, mst_approximation, simulated_annealing
from utils import read_tsp


# def execute_algorithm(file_path, method, seed=None):
#     """Executes a specific TSP solving method."""
#     points = read_tsp(file_path)

#     if not points or len(points) == 0:
#         raise ValueError(f"TSP file {file_path} does not contain valid data")

#     cutoff = 400  # Hard-coded cutoff time
#     name = os.path.basename(file_path).split('.')[0]
#     output_file = f"{name}_{method}_{cutoff}{f'_{seed}' if seed else ''}.sol"

#     if method == "BF":  # Brute Force
#         cost, tour = brute_force.brute_force_tsp(points, cutoff)
#     elif method == "Approx":  # MST Approximation
#         cost, tour = mst_approximation.mst_approximation_tsp(points)
#     elif method == "LS":  # Local Search (Simulated Annealing)
#         if seed is None:
#             raise ValueError("Seed is required for Local Search")
#         cost, tour = simulated_annealing.simulated_annealing_tsp(
#             points, cutoff, seed)
#     else:
#         raise ValueError(f"Unknown method: {method}")

#     # Write results to the output file
#     with open(output_file, 'w') as f:
#         f.write(f"{cost}\n")
#         f.write(",".join(map(str, [points[i][0] for i in tour])))


# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 3 or len(sys.argv) > 4:
#         print("Usage: python exec.py <filename> <method> [<seed>]")
#         sys.exit(1)

#     file_path = sys.argv[1]
#     method = sys.argv[2]
#     seed = int(sys.argv[3]) if len(sys.argv) == 4 else None

#     execute_algorithm(file_path, method, seed)


def execute_algorithm(file_path, method, seed=None):
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

    # Write results to the output file
    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(",".join(map(str, [points[i][0] for i in tour])))


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python exec.py <filename> <method> [<seed>]")
        sys.exit(1)

    file_path = sys.argv[1]
    method = sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) == 4 else None

    execute_algorithm(file_path, method, seed)
