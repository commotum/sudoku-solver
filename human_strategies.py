import numpy as np

def find_naked_singles(candidates, all_deductions):
    N = candidates.shape[0]
    cell_counts = np.sum(candidates, axis=3)  # (N, 9, 9)
    naked_mask = (cell_counts == 1)
    for n in range(N):
        positions = np.argwhere(naked_mask[n])
        for i, j in positions:
            k = np.where(candidates[n, i, j])[0][0]
            all_deductions[n].append({
                'type': 'naked_single',
                'position': (i, j),
                'value': k + 1
            })

def find_hidden_singles_rows(candidates, all_deductions):
    N = candidates.shape[0]
    row_counts = np.sum(candidates, axis=2)  # (N, 9 rows, 9 nums)
    row_hidden_mask = (row_counts == 1)
    for n in range(N):
        for r in range(9):
            for k in range(9):
                if row_hidden_mask[n, r, k]:
                    j = np.where(candidates[n, r, :, k])[0][0]
                    all_deductions[n].append({
                        'type': 'hidden_single_row',
                        'position': (r, j),
                        'value': k + 1
                    })

def find_hidden_singles_cols(candidates, all_deductions):
    N = candidates.shape[0]
    col_counts = np.sum(candidates, axis=1)  # (N, 9 cols, 9 nums)
    col_hidden_mask = (col_counts == 1)
    for n in range(N):
        for c in range(9):
            for k in range(9):
                if col_hidden_mask[n, c, k]:
                    i = np.where(candidates[n, :, c, k])[0][0]
                    all_deductions[n].append({
                        'type': 'hidden_single_col',
                        'position': (i, c),
                        'value': k + 1
                    })

def find_hidden_singles_boxes(candidates, all_deductions):
    N = candidates.shape[0]
    for br in range(3):
        for bc in range(3):
            sub_cand = candidates[:, br*3:(br+1)*3, bc*3:(bc+1)*3, :]
            box_counts = np.sum(sub_cand, axis=(1, 2))  # (N, 9 nums)
            box_hidden_mask = (box_counts == 1)
            for n in range(N):
                for k in range(9):
                    if box_hidden_mask[n, k]:
                        pos = np.argwhere(sub_cand[n, :, :, k])
                        sr, sc = pos[0, 0], pos[0, 1]
                        i, j = br*3 + sr, bc*3 + sc
                        all_deductions[n].append({
                            'type': 'hidden_single_box',
                            'position': (i, j),
                            'value': k + 1
                        })

# Example of adding a new strategy (flesh out as needed)
def find_naked_pairs_rows(candidates, all_deductions):
    # Dummy: Would check rows for two cells with exactly the same two candidates, then eliminate those from other cells in the row.
    # For now, does nothing—implement vectorized detection here.
    pass

# Dictionary mapping strategy names to functions
STRATEGY_FUNCTIONS = {
    'naked_single': find_naked_singles,
    'hidden_single_row': find_hidden_singles_rows,
    'hidden_single_col': find_hidden_singles_cols,
    'hidden_single_box': find_hidden_singles_boxes,
    'naked_pairs_row': find_naked_pairs_rows,  # New one added here
    # Add more as you define them...
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
    
    # Candidates (fixed initialization to (N, 9, 9, 9))
    empty = (grids == 0)
    candidates = np.tile(empty[:, :, :, np.newaxis], (1, 1, 1, 9))
    
    # Apply forbidden
    candidates &= ~row_forbidden[:, :, np.newaxis, :]
    candidates &= ~col_forbidden[:, np.newaxis, :, :]
    
    # Box forbidden per cell
    row_to_box = np.floor_div(np.arange(9), 3)
    box_idx = row_to_box[:, np.newaxis] * 3 + row_to_box[np.newaxis, :]  # (9, 9) with box 0-8
    box_forbidden_per_cell = box_forbidden[:, box_idx, :]  # (N, 9, 9, 9)
    candidates &= ~box_forbidden_per_cell
    
    # Collect deductions per puzzle
    all_deductions = [[] for _ in range(N)]
    
    # Adjust strategies if groups like 'hidden_single' are used
    adjusted_strategies = set()  # Use set to avoid duplicates
    for strat in strategies:
        if strat == 'hidden_single':
            adjusted_strategies.update(['hidden_single_row', 'hidden_single_col', 'hidden_single_box'])
        else:
            adjusted_strategies.add(strat)
    
    # Call each strategy function
    for strat in adjusted_strategies:
        if strat in STRATEGY_FUNCTIONS:
            STRATEGY_FUNCTIONS[strat](candidates, all_deductions)
        else:
            print(f"Warning: Strategy '{strat}' not implemented.")
    
    return all_deductions