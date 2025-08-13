# Core solver: Loads .npy files, solves puzzles using strategies

import os
import numpy as np
from typing import List, Dict
from tqdm import tqdm
from strategies import find_deductions_batch
from utils import is_solved, is_valid, apply_deductions, pretty_print_grid

def format_deduction(pos, val, typ):
    row = chr(ord('A') + int(pos[0]))
    col = int(pos[1]) + 1
    if typ == 'naked_single':
        nice_typ = 'Naked Single'
    elif typ.startswith('hidden_single_'):
        scope = typ.split('_')[-1].title()
        nice_typ = f'Hidden Single - {scope}'
    else:
        nice_typ = typ.replace('_', ' ').title()
    return f"{val} at {row}{col} ({nice_typ})"

def solve_batch(inputs: np.ndarray, outputs: np.ndarray, max_steps: int = 100, verbose: bool = False) -> List[List[Dict]]:
    """
    Solves a batch of Sudoku puzzles using human-like strategies, recording each step.
    
    Args:
        inputs: np.ndarray of shape (N, 9, 9) - initial puzzles.
        outputs: np.ndarray of shape (N, 9, 9) - solutions for validation.
        max_steps: Max iterations to prevent infinite loops.
        verbose: If True, print progress and grids for the first puzzle.
    
    Returns:
        List of sequences, each a list of dicts {'step': i, 'grid_state': flat_grid, 'deductions': [ded_dicts]}.
    """
    N = inputs.shape[0]
    grids = inputs.copy()  # Work on copies
    sequences = [[] for _ in range(N)]
    
    # Strategies to use (start simple, can escalate if needed)
    strategies = ['naked_single', 'hidden_single']  # Add more as implemented
    
    for n in tqdm(range(N), desc="Solving puzzles", disable=not verbose):
        grid = grids[n]
        sequence = sequences[n]
        step = 0
        progress = True
        
        while not is_solved(grid[np.newaxis])[0] and progress and step < max_steps:
            # Find deductions
            deductions = find_deductions_batch(grid[np.newaxis], strategies)[0]
            
            # Record state before applying
            sequence.append({
                'step': step,
                'grid_state': grid.flatten().tolist(),  # Flat for easy serialization
                'deductions': deductions
            })
            
            # For verbose printing with highlighting
            if verbose and n == 0:
                prev_grid = np.copy(grid)
            
            # Apply
            applied = apply_deductions(grid[np.newaxis], [deductions])
            progress = applied > 0
            
            # Print if verbose
            if verbose and n == 0:
                # Deduplicate deductions by position and value
                unique_deds = {}
                for ded in deductions:
                    if 'value' in ded:
                        pos = tuple(map(int, ded['position']))
                        val = int(ded['value'])
                        key = (pos, val)
                        if key not in unique_deds:
                            unique_deds[key] = ded['type']
                
                print(f"T{step + 1}: Δ +{applied}")
                for key, typ in unique_deds.items():
                    pos, val = key
                    print(format_deduction(pos, val, typ))
                print()  # Blank line after deductions
                pretty_print_grid(grid, prev_grid)
            
            step += 1
        
        # Final validation
        if np.array_equal(grid, outputs[n]):
            print(f"Puzzle {n} solved in {step} steps") if verbose else None
        else:
            print(f"Puzzle {n} not fully solved or invalid") if verbose else None
    
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