# Core solver: Loads .npy files, solves puzzles using strategies

import os
import numpy as np
from typing import List, Dict
from strategies import find_deductions_batch
from utils import is_solved, apply_deductions, compute_candidates


def solve_batch(inputs: np.ndarray, outputs: np.ndarray, max_steps: int = 100) -> List[List[Dict]]:
    """
    Solves a batch of Sudoku puzzles using human-like strategies, recording each step.
    
    Args:
        inputs: np.ndarray of shape (N, 9, 9) - initial puzzles.
        outputs: np.ndarray of shape (N, 9, 9) - solutions for validation.
        max_steps: Max iterations to prevent infinite loops.
    
    Returns:
        List of sequences, each a list of dicts {'step': i, 'grid_state': flat_grid, 'deductions': [ded_dicts]}.
    """
    N = inputs.shape[0]
    grids = inputs.copy()  # Work on copies
    sequences = [[] for _ in range(N)]
    
    # Strategies to use (start simple, can escalate if needed)
    strategies = ['naked_single', 'hidden_single', 'subsets', 'intersections', 'fish']

    for n in range(N):
        grid = grids[n]
        sequence = sequences[n]
        candidates = compute_candidates(grid[np.newaxis])
        step = 0
        progress = True

        while not is_solved(grid[np.newaxis])[0] and progress and step < max_steps:
            deductions = find_deductions_batch(strategies=strategies, candidates=candidates)[0]

            sequence.append({
                'step': step,
                'grid_state': grid.flatten().tolist(),
                'deductions': deductions
            })

            applied = apply_deductions(grid[np.newaxis], candidates, [deductions])
            progress = applied > 0

            step += 1

        # Validation can be handled externally if needed
    
    return sequences

def load_and_solve_difficulty(diff: int, data_dir: str = "data/sudoku-extreme-processed", subsample: int = None) -> List[List[Dict]]:
    """
    Loads inputs/outputs for a difficulty level and solves them.
    
    Args:
        diff: Difficulty level.
        data_dir: Path to data.
        subsample: Optional number to subsample puzzles.
    
    Returns:
        Sequences for the batch.
    """
    inputs_path = os.path.join(data_dir, f"lvl-{diff}-inputs.npy")
    outputs_path = os.path.join(data_dir, f"lvl-{diff}-outputs.npy")
    
    if not os.path.exists(inputs_path):
        raise FileNotFoundError(f"No data for level {diff}")
    
    inputs = np.load(inputs_path)
    outputs = np.load(outputs_path)
    
    if subsample:
        inputs = inputs[:subsample]
        outputs = outputs[:subsample]
    
    return solve_batch(inputs, outputs)
