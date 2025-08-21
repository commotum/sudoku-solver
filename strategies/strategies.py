import numpy as np

# --- imports (deduped; keep optional ones commented until implemented) ---
from .singles import (
    find_naked_singles,
    find_hidden_singles_rows,
    find_hidden_singles_cols,
    find_hidden_singles_boxes,
)

from .intersections import (
    find_locked_candidates_pointing,
    find_locked_candidates_claiming,
)

from .subsets import find_naked_subsets, find_hidden_subsets

from .fish import (
    find_x_wing_rows, find_x_wing_cols,
    find_swordfish_rows, find_swordfish_cols,
    find_jellyfish_rows, find_jellyfish_cols,
)

from .uniqueness import (
    find_ur_type1, find_ur_type2, find_ur_type2b,
    find_ur_type3, find_ur_type4,
)
# Optional (enable if you have them)
# from .bug import find_bug
# from .wings import find_xy_wing, find_xyz_wing, find_w_wing


STRATEGY_FUNCTIONS = {
    # Singles
    "naked_single": find_naked_singles,
    "hidden_single_row": find_hidden_singles_rows,
    "hidden_single_col": find_hidden_singles_cols,
    "hidden_single_box": find_hidden_singles_boxes,

    # Intersections & Subsets
    "locked_pointing": find_locked_candidates_pointing,
    "locked_claiming": find_locked_candidates_claiming,
    "naked_subsets": find_naked_subsets,
    "hidden_subsets": find_hidden_subsets,

    # Uniqueness
    "ur_type1": find_ur_type1,
    "ur_type2": find_ur_type2,
    "ur_type2b": find_ur_type2b,
    "ur_type3": find_ur_type3,
    "ur_type4": find_ur_type4,
    # "bug": find_bug,

    # Advanced (fish / wings / other)
    "x_wing_row": find_x_wing_rows,
    "x_wing_col": find_x_wing_cols,
    "swordfish_row": find_swordfish_rows,
    "swordfish_col": find_swordfish_cols,
    "jellyfish_row": find_jellyfish_rows,
    "jellyfish_col": find_jellyfish_cols,
    # "xy_wing": find_xy_wing,
    # "xyz_wing": find_xyz_wing,
    # "w_wing": find_w_wing,
}

TIERS = {
    # Tier 1 — Singles (cheapest; always first)
    1: [
        "naked_single",
        "hidden_single_row", "hidden_single_col", "hidden_single_box",
    ],

    # Tier 2 — Core Subsets (intersections then subsets)
    # Run locking first to simplify candidate sets for subsets.
    2: [
        "locked_pointing", "locked_claiming",
        "naked_subsets", "hidden_subsets",
    ],

    # Tier 3 — Uniqueness & BUG (safety nets; early–mid)
    # Light UR before heavy/advanced; BUG first if you have it.
    3: [
        # "bug",
        "ur_type1", "ur_type2", "ur_type2b",
    ],

    # Tier 4 — Advanced (fish/wings/other)
    # Escalate by size: X-Wing → Swordfish → Jellyfish; then heavy UR.
    4: [
        "x_wing_row", "x_wing_col",
        "swordfish_row", "swordfish_col",
        "jellyfish_row", "jellyfish_col",
        # "xy_wing", "xyz_wing", "w_wing",
        "ur_type3", "ur_type4",
    ],

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
