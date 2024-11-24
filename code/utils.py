# utils.py
import math


import os


def read_tsp(file_path):
    """Parses a .tsp file and extracts points as a list of (id, x, y)."""
    # Ensure the file path is correct relative to this script's directory
    full_path = os.path.join(os.path.dirname(__file__), "..", file_path)
    points = []

    try:
        with open(full_path, 'r') as f:
            lines = f.readlines()

        # Debugging: Print all lines for verification
        # print("DEBUG: File lines:\n", lines)

        # Skip the first 5 lines and process the coordinate section
        for line in lines[5:]:
            line = line.strip()

            if line == "EOF":  # Stop parsing at "EOF"
                break

            parts = line.split()
            if len(parts) == 3:  # Ensure it has id, x, y
                node_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                points.append((node_id, x, y))
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {full_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading TSP file {full_path}: {e}")

    # Debugging: Print the parsed points for verification
    # print(f"DEBUG: Parsed points: {points}")

    return points


def create_distance_matrix(points):
    """Creates a distance matrix from points."""
    n = len(points)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            matrix[i][j] = matrix[j][i] = dist
    return matrix


def euclidean_distance(p1, p2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
