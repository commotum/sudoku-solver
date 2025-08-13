import numpy as np
from .singles import (
    find_naked_singles,
    find_hidden_singles_rows,
    find_hidden_singles_cols,
    find_hidden_singles_boxes,
)
from .subsets import find_naked_subsets, find_hidden_subsets
from .intersections import find_locked_candidates_pointing, find_locked_candidates_claiming

# Dictionary mapping strategy names to functions
STRATEGY_FUNCTIONS = {
    'naked_single': find_naked_singles,
    'hidden_single_row': find_hidden_singles_rows,
    'hidden_single_col': find_hidden_singles_cols,
    'hidden_single_box': find_hidden_singles_boxes,
    'naked_subsets': find_naked_subsets,
    'hidden_subsets': find_hidden_subsets,
    'locked_pointing': find_locked_candidates_pointing,
    'locked_claiming': find_locked_candidates_claiming,
    # Add more from other files as we implement them, e.g., from fish.py
}

def find_deductions_batch(grids: np.ndarray, strategies: list[str] = ['naked_single', 'hidden_single']) -> list[list[dict]]:
    """
    Finds deductions using multiple strategies in a batch of Sudoku grids.
    
    Args:
        grids: np.ndarray of shape (N, 9, 9) with values 0-9 (0 for empty).
        strategies: List of strategy names to check (e.g., ['naked_single', 'hidden_single']).
    
    Returns:
        List of lists: for each puzzle, a list of dicts like 
        {'type': strategy_name, 'position': (row, col), 'value': val}.
    """
    N = grids.shape[0]
    if grids.shape[1:] != (9, 9):
        raise ValueError("Grids must be (N, 9, 9)")
    
    # Compute forbidden masks: vectorized over N
    row_forbidden = np.stack([np.any(grids == k, axis=2) for k in range(1, 10)], axis=-1)  # (N, 9 rows, 9 nums)
    col_forbidden = np.stack([np.any(grids == k, axis=1) for k in range(1, 10)], axis=-1)  # (N, 9 cols, 9 nums)
    
    # Box forbidden
    box_forbidden = np.zeros((N, 9, 9), dtype=bool)  # (N, 9 boxes, 9 nums)
    for br in range(3):
        for bc in range(3):
            subgrid = grids[:, br*3:(br+1)*3, bc*3:(bc+1)*3]
            box_idx = br * 3 + bc
            for k in range(1, 10):
                box_forbidden[:, box_idx, k-1] = np.any(subgrid == k, axis=(1, 2))
    
    # Candidates
    empty = (grids == 0)
    candidates = np.tile(empty[:, :, :, np.newaxis], (1, 1, 1, 9))
    
    # Apply forbidden
    candidates &= ~row_forbidden[:, :, np.newaxis, :]
    candidates &= ~col_forbidden[:, np.newaxis, :, :]
    
    # Box forbidden per cell
    row_to_box = np.floor_divide(np.arange(9), 3)
    box_idx = row_to_box[:, np.newaxis] * 3 + row_to_box[np.newaxis, :]  # (9, 9) with box 0-8
    box_forbidden_per_cell = box_forbidden[:, box_idx, :]  # (N, 9, 9, 9)
    candidates &= ~box_forbidden_per_cell
    
    # Collect deductions per puzzle
    all_deductions = [[] for _ in range(N)]
    
    # Adjust strategies if groups like 'hidden_single' are used
    adjusted_strategies = set()
    for strat in strategies:
        if strat == 'hidden_single':
            adjusted_strategies.update(['hidden_single_row', 'hidden_single_col', 'hidden_single_box'])
        elif strat == 'subsets':
            adjusted_strategies.update(['naked_subsets', 'hidden_subsets'])
        elif strat == 'intersections':
            adjusted_strategies.update(['locked_pointing', 'locked_claiming'])
        else:
            adjusted_strategies.add(strat)
    
    # Call each strategy function
    for strat in adjusted_strategies:
        if strat in STRATEGY_FUNCTIONS:
            STRATEGY_FUNCTIONS[strat](candidates, all_deductions)
        else:
            print(f"Warning: Strategy '{strat}' not implemented.")
    
    return all_deductions