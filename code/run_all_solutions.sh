#!/bin/bash

# Ensure we're in the directory containing exec.py
cd "$(dirname "$0")"

# Input and output directories
INPUT_DIR="../input"
OUTPUT_DIR="../output"

# Create the output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Algorithms to run
ALGORITHMS=("BF" "Approx" "LS")
SEED=42  # Random seed for Local Search

# Loop through all .tsp files in the input directory
for FILE in $INPUT_DIR/*.tsp; do
    FILENAME=$(basename $FILE)               # Extract file name (e.g., Atlanta.tsp)
    INSTANCE="${FILENAME%.*}"               # Strip the file extension (e.g., Atlanta)

    echo "Processing instance: $INSTANCE"

    # Run each algorithm
    for METHOD in "${ALGORITHMS[@]}"; do
        if [ "$METHOD" = "LS" ]; then
            # Local Search requires a seed
            echo "Running $METHOD on $INSTANCE with seed $SEED"
            python -m exec $FILE $METHOD $SEED
        else
            # Brute Force and MST Approximation
            echo "Running $METHOD on $INSTANCE"
            python -m exec $FILE $METHOD
        fi
    done
done

echo "All solutions have been computed and saved in $OUTPUT_DIR."
