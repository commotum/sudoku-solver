# Entry point: Args for difficulty levels/subsample, calls dataset_download if needed, then solver

import numpy as np
import random
import datetime
from solver import solve_batch
from utils import display_sequence

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
    
    print()
    print(f"Selected puzzle index: {idx} from level {level} (out of {num_puzzles} puzzles)")
    print()
    
    sequences = solve_batch(selected_input, selected_output)

    # Display the step-by-step solution
    print("Solving sequence:")
    print()
    display_sequence(selected_input[0], sequences[0])

if __name__ == "__main__":
    main()
