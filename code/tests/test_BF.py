# test_brute_force_empty_input.py
from algorithms.brute_force import brute_force_tsp
from utils import read_tsp


def test_brute_force_empty_input():
    try:
        brute_force_tsp([], 10)  # Pass empty points
    except ValueError as e:
        assert str(e) == "No points provided for TSP", f"Unexpected error: {e}"
        print("Test passed: Correctly handled empty input")


if __name__ == "__main__":
    test_brute_force_empty_input()
