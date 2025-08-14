import numpy as np
from lattice_utils import init_lattice, fill_cell, eliminate
from strategies import find_deductions, TIERS


def apply_deductions(grid: np.ndarray, lattice: np.ndarray, deductions: list[dict]) -> int:
    changes = 0
    for ded in deductions:
        if 'value' in ded and 'position' in ded:
            r, c = ded['position']
            v = ded['value']
            if grid[r, c] == 0:
                fill_cell(grid, lattice, r, c, v)
                changes += 1
        if 'eliminations' in ded:
            for (r, c), vals in ded['eliminations']:
                for v in vals:
                    if lattice[r, c, v - 1]:
                        lattice[r, c, v - 1] = False
                        changes += 1
    return changes


def solve(grid: np.ndarray, max_steps: int = 100, max_tier: int = 5):
    lattice = init_lattice(grid)
    steps = []
    step = 0
    while step < max_steps and (grid == 0).any():
        progress = False
        for tier in range(1, max_tier + 1):
            deductions = find_deductions(lattice, grid, TIERS[tier])
            if not deductions:
                continue
            changed = apply_deductions(grid, lattice, deductions)
            if changed:
                steps.append({'step': step, 'tier': tier, 'deductions': deductions, 'grid': grid.copy()})
                progress = True
                break
        if not progress:
            break
        step += 1
    return grid, steps


def main():
    puzzle = np.array([
        [8, 3, 7, 0, 0, 1, 0, 0, 6],
        [6, 1, 4, 0, 7, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 2, 4, 3, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 6, 0],
        [0, 7, 0, 6, 0, 0, 2, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 2, 9],
        [0, 0, 5, 8, 0, 0, 6, 0, 0],
        [0, 9, 0, 0, 0, 4, 7, 0, 5],
    ])
    solved, steps = solve(puzzle)
    print(solved)
    print(f"Solved in {len(steps)} steps")


if __name__ == '__main__':
    main()
