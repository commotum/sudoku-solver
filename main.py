# Entry point: Args for difficulty levels/subsample, calls dataset_download if needed, then solver

import argparse
import numpy as np
import random
import datetime
from solver import solve_batch
from display import (
    display_sequence,
    print_program_header,
    print_puzzle_selection,
    print_initial_grid,
    print_step_header,
    print_final_output,
)

def main():
    parser = argparse.ArgumentParser(description="Run the Sudoku solver")
    parser.add_argument(
        "--level",
        type=int,
        default=0,
        help="Difficulty level to choose from",
    )
    args = parser.parse_args()
    level = args.level

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

    selected_input = inputs[idx : idx + 1]
    selected_output = outputs[idx : idx + 1]

    print_program_header()
    print_puzzle_selection(level, num_puzzles, idx)
    print_initial_grid(selected_input[0])

    sequences, solved_flags = solve_batch(selected_input, selected_output)

    print_step_header()

    # Display the step-by-step solution and gather summary
    final_grid, steps, total_placements = display_sequence(
        selected_input[0], sequences[0]
    )

    print_final_output(final_grid, steps, total_placements, solved_flags[0])

if __name__ == "__main__":
    main()
