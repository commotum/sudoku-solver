import numpy as np
from .singles import (
    find_naked_singles,
    find_hidden_singles_rows,
    find_hidden_singles_cols,
    find_hidden_singles_boxes,
)
from .subsets import find_naked_subsets, find_hidden_subsets
from .intersections import (
    find_locked_candidates_pointing,
    find_locked_candidates_claiming,
)
from .fish import (
    find_x_wing_rows,
    find_x_wing_cols,
    find_swordfish_rows,
    find_swordfish_cols,
)
from engine.utils import compute_candidates
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
    'x_wing_row': find_x_wing_rows,
    'x_wing_col': find_x_wing_cols,
    'swordfish_row': find_swordfish_rows,
    'swordfish_col': find_swordfish_cols,
}

# Strategy tiers from easiest to hardest. Each tier is a pre-expanded list of
# explicit strategy names in deterministic execution order.
TIERS = {
    1: [
        'naked_single',
        'hidden_single_row',
        'hidden_single_col',
        'hidden_single_box',
    ],
    2: [
        'naked_subsets',
        'hidden_subsets',
        'locked_pointing',
        'locked_claiming',
    ],
    3: [
        'x_wing_row',
        'x_wing_col',
        'swordfish_row',
        'swordfish_col',
    ],
    # Placeholders for future strategy categories
    4: [],  # wings
    5: [],  # chains
}

def find_deductions_batch(
    grids: np.ndarray | None = None,
    strategies: list[str] = [
        'naked_single',
        'hidden_single_row',
        'hidden_single_col',
        'hidden_single_box',
    ],
    candidates: np.ndarray | None = None,
) -> list[list[dict]]:
    """Find deductions for a batch of Sudoku grids or candidate masks."""
    if candidates is None:
        if grids is None:
            raise ValueError("Either grids or candidates must be provided")
        candidates = compute_candidates(grids)

    N = candidates.shape[0]

    all_deductions = [[] for _ in range(N)]

    for strat in strategies:
        if strat in STRATEGY_FUNCTIONS:
            STRATEGY_FUNCTIONS[strat](candidates, all_deductions)
        else:
            print(f"Warning: Strategy '{strat}' not implemented.")

    return all_deductions
