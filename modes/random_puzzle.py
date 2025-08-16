import argparse
import numpy as np
import random
from display import pretty_print_grid

def main():
    parser = argparse.ArgumentParser(description="Pretty print a random Sudoku puzzle from a given difficulty level")
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

    inputs = np.load(inputs_path)
    num_puzzles = inputs.shape[0]

    idx = random.randint(0, num_puzzles - 1)
    puzzle = inputs[idx]

    print(f"Difficulty Level: {level}")
    print(f"Total Puzzles at Level: {num_puzzles}")
    print(f"Randomly Selected Puzzle Index: {idx}\n")
    pretty_print_grid(puzzle)

if __name__ == "__main__":
    main()
