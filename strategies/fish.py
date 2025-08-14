import numpy as np
from itertools import combinations


def _fish(lattice: np.ndarray, size: int, orient: str) -> list[dict]:
    deductions: list[dict] = []
    if orient == 'row':
        line_axis = 0
        cross_axis = 1
    else:
        line_axis = 1
        cross_axis = 0
    for k in range(9):
        lines = []
        for idx in range(9):
            if orient == 'row':
                positions = np.where(lattice[idx, :, k])[0]
            else:
                positions = np.where(lattice[:, idx, k])[0]
            if 2 <= len(positions) <= size:
                lines.append((idx, positions))
        for combo in combinations(lines, size):
            indices = [x[0] for x in combo]
            union = np.unique(np.concatenate([x[1] for x in combo]))
            if len(union) != size:
                continue
            elims = []
            for pos in union:
                for other in set(range(9)) - set(indices):
                    r, c = (other, pos) if orient == 'row' else (pos, other)
                    if lattice[r, c, k]:
                        elims.append(((r, c), [k + 1]))
            if elims:
                deductions.append({'type': f'{"x_wing" if size==2 else "swordfish"}_{orient}',
                                   'value': k + 1,
                                   'lines': indices,
                                   'cross': union.tolist(),
                                   'eliminations': elims})
    return deductions


def x_wing(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    return _fish(lattice, 2, 'row') + _fish(lattice, 2, 'col')


def swordfish(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    return _fish(lattice, 3, 'row') + _fish(lattice, 3, 'col')
