# Entry point: Args for difficulty levels/subsample, calls dataset_download if needed, then solver

import numpy as np
import random
import datetime
from solver import solve_batch
from utils import display_sequence, pretty_print_grid

def main():
    level = 0
    data_dir = "data/sudoku-extreme-processed"
    inputs_path = f"{data_dir}/lvl-{level}-inputs.npy"
    outputs_path = f"{data_dir}/lvl-{level}-outputs.npy"
    
    inputs = np.load(inputs_path)
    outputs = np.load(outputs_path)
    
    num_puzzles = inputs.shape[0]
    
    # Seed random with date for reproducible "daily" selection
    today = datetime.date.today()
    random.seed(today.toordinal())
    
    idx = random.randint(0, num_puzzles - 1)
    
    selected_input = inputs[idx:idx+1]
    selected_output = outputs[idx:idx+1]

    # Header and puzzle selection info
    print()
    print("====================================")
    print("Sudoku Solver v1.0")
    print("====================================")
    print()
    print("Puzzle Chosen:")
    print(f"- Difficulty Level: {level}")
    print(f"- Puzzles @ Level : {num_puzzles-1}")
    print(f"- Selected Puzzle : {idx}")
    print()
    print("Initial Puzzle Grid:")
    pretty_print_grid(selected_input[0])
    print()

    sequences = solve_batch(selected_input, selected_output)

    print("====================================")
    print("Step by Step Solution:")
    print("====================================")
    print()

    # Display the step-by-step solution and gather summary
    final_grid, steps, total_placements = display_sequence(selected_input[0], sequences[0])

    print("====================================")
    print("Final Grid:")
    print("====================================")
    print()
    pretty_print_grid(final_grid)
    print()
    print("Puzzle Solved!")
    print(f"- Total Steps: {steps}")
    print(f"- Total Placements: {total_placements}")
    print()
    print("====================================")
    print("PROGRAM END.")
    print("====================================")
    print()

if __name__ == "__main__":
    main()
