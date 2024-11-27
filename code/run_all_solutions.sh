#!/bin/bash

# Ensure the script runs in the directory containing exec.py
cd "$(dirname "$0")"

# Input and output directories
INPUT_DIR="input"
OUTPUT_DIR="output"

# Create the output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Algorithms to run
ALGORITHMS=("BF" "Approx" "LS")

# Cutoff times to test
CUTOFFS=(100 200 300)

# Number of runs for Local Search (LS) with different seeds
NUM_LS_RUNS=10

# Loop through all .tsp files in the input directory
for FILE in $INPUT_DIR/*.tsp; do
    FILENAME=$(basename $FILE)               # Extract file name (e.g., Atlanta.tsp)
    INSTANCE="${FILENAME%.*}"               # Strip the file extension (e.g., Atlanta)

    echo "Processing instance: $INSTANCE"

    # Run each algorithm
    for METHOD in "${ALGORITHMS[@]}"; do
        for CUTOFF in "${CUTOFFS[@]}"; do
            if [ "$METHOD" = "LS" ]; then
                # Local Search: Run multiple times with different seeds
                echo "Running $METHOD on $INSTANCE with cutoff $CUTOFF and multiple seeds"
                for SEED in $(seq 1 $NUM_LS_RUNS); do
                    echo "  Seed $SEED"
                    python -m exec -inst $FILE -alg $METHOD -time $CUTOFF -seed $SEED
                done
            else
                # Brute Force and MST Approximation
                echo "Running $METHOD on $INSTANCE with cutoff $CUTOFF"
                python -m exec -inst $FILE -alg $METHOD -time $CUTOFF
            fi
        done
    done
done

echo "All solutions have been computed and saved in $OUTPUT_DIR."
