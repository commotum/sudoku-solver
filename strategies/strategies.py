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
    find_jellyfish_rows,
    find_jellyfish_cols,
)
from .uniqueness import find_ur_type1

STRATEGY_FUNCTIONS = {
    "naked_single": find_naked_singles,
    "hidden_single_row": find_hidden_singles_rows,
    "hidden_single_col": find_hidden_singles_cols,
    "hidden_single_box": find_hidden_singles_boxes,
    "naked_subsets": find_naked_subsets,
    "hidden_subsets": find_hidden_subsets,
    "locked_pointing": find_locked_candidates_pointing,
    "locked_claiming": find_locked_candidates_claiming,
    "x_wing_row": find_x_wing_rows,
    "x_wing_col": find_x_wing_cols,
    "swordfish_row": find_swordfish_rows,
    "swordfish_col": find_swordfish_cols,
    "jellyfish_row": find_jellyfish_rows,
    "jellyfish_col": find_jellyfish_cols,
    "ur_type1": find_ur_type1,
}

TIERS = {
    1: [
        "naked_single",
        "hidden_single_row",
        "hidden_single_col",
        "hidden_single_box",
    ],
    2: [
        "naked_subsets",
        "hidden_subsets",
        "locked_pointing",
        "locked_claiming",
    ],
    3: [
        "x_wing_row",
        "x_wing_col",
        "swordfish_row",
        "swordfish_col",
        "jellyfish_row",
        "jellyfish_col",
        "ur_type1",
    ],
    4: [],
    5: [],
}

def find_deductions_batch(mask: np.ndarray, strategies: list[str]) -> list[list[dict]]:
    """Run selected strategies on mask batch."""
    if mask.ndim == 3:
        mask = mask[None, ...]
    N = mask.shape[0]
    all_deductions = [[] for _ in range(N)]
    for name in strategies:
        func = STRATEGY_FUNCTIONS.get(name)
        if func:
            func(mask, all_deductions)
        else:
            print(f"Warning: Strategy '{name}' not implemented.")
    return all_deductions
