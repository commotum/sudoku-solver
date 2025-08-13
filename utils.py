# Helpers: Grid validation, pretty-print, apply_deduction, candidate computation

import numpy as np

def is_solved(grids: np.ndarray) -> np.ndarray:
    """
    Checks if each puzzle in the batch is fully solved (all cells filled with 1-9, no zeros).
    
    Args:
        grids: np.ndarray of shape (N, 9, 9).
    
    Returns:
        np.ndarray of shape (N,) with bools: True if solved.
    """
    return np.all(grids != 0, axis=(1, 2))

def is_valid(grids: np.ndarray) -> np.ndarray:
    """
    Validates each puzzle in the batch: No duplicates in rows, columns, or boxes (ignoring zeros).
    
    Args:
        grids: np.ndarray of shape (N, 9, 9).
    
    Returns:
        np.ndarray of shape (N,) with bools: True if valid (no conflicts).
    """
    N = grids.shape[0]
    valid = np.ones(N, dtype=bool)
    
    # Check rows
    for i in range(9):
        row_vals = grids[:, i, :]
        for n in range(N):
            if not valid[n]:
                continue
            non_zero = row_vals[n][row_vals[n] != 0]
            if len(non_zero) != len(np.unique(non_zero)):
                valid[n] = False
    
    # Check columns
    for j in range(9):
        col_vals = grids[:, :, j]
        for n in range(N):
            if not valid[n]:
                continue
            non_zero = col_vals[n][col_vals[n] != 0]
            if len(non_zero) != len(np.unique(non_zero)):
                valid[n] = False
    
    # Check boxes
    for br in range(3):
        for bc in range(3):
            subgrids = grids[:, br*3:(br+1)*3, bc*3:(bc+1)*3]
            for n in range(N):
                if not valid[n]:
                    continue
                flat = subgrids[n].flatten()
                non_zero = flat[flat != 0]
                if len(non_zero) != len(np.unique(non_zero)):
                    valid[n] = False
    
    return valid

def apply_deductions(grids: np.ndarray, all_deductions: list[list[dict]]) -> int:
    """
    Applies fill deductions (certainties) to the grids in the batch. Only handles 'value' fills for now.
    Skips if cell is already filled or invalid move (though strategies should prevent conflicts).
    
    Args:
        grids: np.ndarray of shape (N, 9, 9) to modify in-place.
        all_deductions: List of lists from find_deductions_batch.
    
    Returns:
        Total number of deductions applied across all puzzles.
    """
    N = grids.shape[0]
    applied_count = 0
    
    for n in range(N):
        for ded in all_deductions[n]:
            if 'value' in ded:  # For singles (fills)
                i, j = ded['position']
                val = ded['value']
                if grids[n, i, j] == 0:  # Only apply if empty
                    grids[n, i, j] = val
                    applied_count += 1
                # TODO: Add conflict check if needed, but assume strategies are correct
    
    return applied_count

def pretty_print_grid(grid: np.ndarray, prev_grid: np.ndarray = None):
    """
    Pretty-prints a single 9x9 grid using box drawing characters.
    If prev_grid is provided, new numbers (changes from 0 to a value) are printed in red.
    
    Args:
        grid: np.ndarray of shape (9, 9).
        prev_grid: Optional np.ndarray of shape (9, 9) for highlighting new cells.
    """
    RED = '\033[31m'
    RESET = '\033[0m'
    
    print('┌───────┬───────┬───────┐')
    for i in range(9):
        row_parts = []
        for block in range(3):
            block_cells = []
            for j in range(3):
                col = block * 3 + j
                cell = grid[i, col]
                val = str(cell) if cell != 0 else '.'
                if prev_grid is not None and grid[i, col] != prev_grid[i, col] and cell != 0:
                    val = RED + val + RESET
                block_cells.append(val)
            row_parts.append(' '.join(block_cells))
        print('│ ' + ' │ '.join(row_parts) + ' │')
        if (i + 1) % 3 == 0 and i != 8:
            print('├───────┼───────┼───────┤')
    print('└───────┴───────┴───────┘')


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


def display_sequence(initial_grid: np.ndarray, sequence: list[dict]):
    """Replay a solution sequence with pretty printing and summary statistics.

    Args:
        initial_grid: Starting grid for the puzzle.
        sequence: List of step dictionaries returned by ``solve_batch``.

    Returns:
        tuple containing the final grid, number of steps, and total placements.
    """
    grid = initial_grid.copy()
    total_placements = 0

    print("Solving Process:")
    print("----------------")

    for step_info in sequence:
        deductions = step_info['deductions']
        prev_grid = grid.copy()
        applied = apply_deductions(grid[np.newaxis], [deductions])
        total_placements += applied

        print(f"T-{step_info['step'] + 1}:  Δ +{applied}")

        unique_deds = {}
        for ded in deductions:
            if 'value' in ded:
                pos = tuple(map(int, ded['position']))
                val = int(ded['value'])
                key = (pos, val)
                if key not in unique_deds:
                    unique_deds[key] = ded['type']

        for key, typ in unique_deds.items():
            pos, val = key
            print(format_deduction(pos, val, typ))

        print()
        pretty_print_grid(grid, prev_grid)

    print("----------------")

    return grid, len(sequence), total_placements