import numpy as np
from .singles import naked_single, hidden_single
from .subsets import naked_subsets, hidden_subsets
from .intersections import locked_candidates_pointing, locked_candidates_claiming
from .fish import x_wing, swordfish
from .wings import xy_wing, xyz_wing
from .chains import simple_coloring

STRATEGY_FUNCTIONS = {
    'naked_single': naked_single,
    'hidden_single': hidden_single,
    'naked_subsets': naked_subsets,
    'hidden_subsets': hidden_subsets,
    'locked_pointing': locked_candidates_pointing,
    'locked_claiming': locked_candidates_claiming,
    'x_wing': x_wing,
    'swordfish': swordfish,
    'xy_wing': xy_wing,
    'xyz_wing': xyz_wing,
    'simple_coloring': simple_coloring,
}

TIERS = {
    1: ['naked_single', 'hidden_single'],
    2: ['naked_subsets', 'hidden_subsets', 'locked_pointing', 'locked_claiming'],
    3: ['x_wing', 'swordfish'],
    4: ['xy_wing', 'xyz_wing'],
    5: ['simple_coloring'],
}

def find_deductions(lattice: np.ndarray, grid: np.ndarray, strategies: list[str]) -> list[dict]:
    deductions: list[dict] = []
    for name in strategies:
        func = STRATEGY_FUNCTIONS.get(name)
        if func is None:
            continue
        deductions.extend(func(lattice, grid))
    return deductions
