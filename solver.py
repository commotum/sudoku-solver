# Core solver: Loads .npy files, solves puzzles using strategies

import os
import numpy as np
from typing import List, Dict
from strategies import find_deductions_batch, TIERS
from utils import is_solved, apply_deductions, compute_candidates


def solve_batch(
    inputs: np.ndarray, outputs: np.ndarray, max_steps: int = 100, max_tier: int = 3
) -> List[List[Dict]]:
    """Solve a batch of Sudoku puzzles using ordered strategy tiers.

    The solver applies strategies in increasing difficulty.  At each step it
    exhausts the current tier and only escalates when no progress is made.
    Certainty fills (singles) are applied before eliminations.

    Args:
        inputs: np.ndarray of shape (N, 9, 9) - initial puzzles.
        outputs: np.ndarray of shape (N, 9, 9) - solutions for validation.
        max_steps: Max iterations per puzzle.
        max_tier: Highest strategy tier to use (see strategies.TIERS).

    Returns:
        List of sequences, each a list of dictionaries describing the steps
        taken to solve a puzzle.
    """
    N = inputs.shape[0]
    grids = inputs.copy()  # Work on copies
    sequences = [[] for _ in range(N)]

    for n in range(N):
        grid = grids[n]
        sequence = sequences[n]
        step = 0

        while not is_solved(grid[np.newaxis])[0] and step < max_steps:
            candidates = compute_candidates(grid[np.newaxis])
            progress = False

            for tier in range(1, max_tier + 1):
                tier_strategies = TIERS[tier]
                deductions = find_deductions_batch(
                    strategies=tier_strategies, candidates=candidates
                )[0]

                fills = [d for d in deductions if 'value' in d]
                if fills:
                    sequence.append(
                        {
                            'step': step,
                            'grid_state': grid.flatten().tolist(),
                            'deductions': fills,
                        }
                    )
                    apply_deductions(grid[np.newaxis], candidates, [fills])
                    progress = True
                    break

                elims = [d for d in deductions if 'eliminations' in d]
                if elims:
                    sequence.append(
                        {
                            'step': step,
                            'grid_state': grid.flatten().tolist(),
                            'deductions': elims,
                        }
                    )
                    apply_deductions(grid[np.newaxis], candidates, [elims])
                    progress = True
                    break

            if not progress:
                break

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

    # Escalate allowed strategies based on difficulty
    if diff <= 2:
        max_tier = 1
    elif diff <= 5:
        max_tier = 2
    else:
        max_tier = 3

    return solve_batch(inputs, outputs, max_tier=max_tier)
