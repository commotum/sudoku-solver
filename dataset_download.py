import os
import csv
import json
import numpy as np
from typing import Dict, List, Tuple
from huggingface_hub import hf_hub_download
from tqdm import tqdm

# Configuration (hardcoded for now, can be made configurable later)
SOURCE_REPO = "sapientinc/sudoku-extreme"
OUTPUT_DIR = "data/sudoku-extreme-processed"
SETS = ["train", "test"]  # Process both train and test CSVs

def download_and_process_datasets() -> Dict[int, Tuple[List[np.ndarray], List[np.ndarray]]]:
    """
    Downloads the Sudoku datasets from Hugging Face, processes them into 9x9 numpy arrays,
    determines the min and max difficulty levels, and groups inputs/outputs by difficulty level.
    
    Returns a dictionary where keys are difficulty levels (integers), and values are tuples of
    (inputs_list, outputs_list), each being lists of 9x9 np.uint8 arrays.
    """
    all_inputs = []
    all_outputs = []
    all_ratings = []
    
    # Download and read each CSV
    for set_name in SETS:
        csv_path = hf_hub_download(SOURCE_REPO, f"{set_name}.csv", repo_type="dataset")
        
        with open(csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header (source, q, a, rating)
            for source, q, a, rating in tqdm(reader, desc=f"Processing {set_name} set"):
                # Assert lengths
                assert len(q) == 81 and len(a) == 81, f"Invalid puzzle length in {set_name} set"
                
                # Convert q to 9x9 array (blanks as 0)
                input_arr = np.frombuffer(q.replace('.', '0').encode(), dtype=np.uint8).reshape(9, 9) - ord('0')
                # Convert a to 9x9 array
                output_arr = np.frombuffer(a.encode(), dtype=np.uint8).reshape(9, 9) - ord('0')
                
                all_inputs.append(input_arr)
                all_outputs.append(output_arr)
                all_ratings.append(int(rating))
    
    # Determine min and max difficulty
    if not all_ratings:
        raise ValueError("No puzzles found in datasets")
    min_diff = min(all_ratings)
    max_diff = max(all_ratings)
    print(f"Difficulty range: {min_diff} to {max_diff}")
    
    # Create buckets for each difficulty level
    buckets: Dict[int, Tuple[List[np.ndarray], List[np.ndarray]]] = {}
    for diff in range(min_diff, max_diff + 1):
        buckets[diff] = ([], [])  # (inputs, outputs)
    
    # Assign puzzles to buckets
    for inp, out, rating in zip(all_inputs, all_outputs, all_ratings):
        inputs_list, outputs_list = buckets[rating]
        inputs_list.append(inp)
        outputs_list.append(out)
    
    return buckets

def save_buckets(buckets: Dict[int, Tuple[List[np.ndarray], List[np.ndarray]]]):
    """
    Saves the grouped inputs and outputs as numpy files in the output directory.
    For each difficulty level, saves:
    - lvl-<diff>-inputs.npy: stacked array of shape (num_puzzles, 9, 9)
    - lvl-<diff>-outputs.npy: stacked array of shape (num_puzzles, 9, 9)
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for diff, (inputs_list, outputs_list) in buckets.items():
        if inputs_list:
            inputs_array = np.stack(inputs_list)  # Shape: (num_puzzles, 9, 9)
            outputs_array = np.stack(outputs_list)  # Shape: (num_puzzles, 9, 9)
            
            np.save(os.path.join(OUTPUT_DIR, f"lvl-{diff}-inputs.npy"), inputs_array)
            np.save(os.path.join(OUTPUT_DIR, f"lvl-{diff}-outputs.npy"), outputs_array)
            print(f"Saved level {diff}: {len(inputs_list)} puzzles")

if __name__ == "__main__":
    buckets = download_and_process_datasets()
    save_buckets(buckets)