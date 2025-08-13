# SPDX-License-Identifier: MIT
"""Fish strategies: X-Wing and Swordfish."""

import numpy as np
from itertools import combinations


def _find_fish(candidates: np.ndarray, all_deductions: list[list[dict]], size: int, orientation: str):
    N = candidates.shape[0]
    for n in range(N):
        cand = candidates[n]
        for k in range(9):
            if orientation == 'row':
                positions = [np.where(cand[r, :, k])[0] for r in range(9)]
                base_indices = [r for r in range(9) if 2 <= len(positions[r]) <= size]
                for rows in combinations(base_indices, size):
                    union_cols = set().union(*(set(positions[r]) for r in rows))
                    if len(union_cols) != size:
                        continue
                    base_positions = []
                    for r in rows:
                        for c in positions[r]:
                            base_positions.append((r, c))
                    eliminations = []
                    for c in sorted(union_cols):
                        for r in range(9):
                            if r in rows:
                                continue
                            if cand[r, c, k]:
                                eliminations.append(((r, c), [k + 1]))
                    if eliminations:
                        all_deductions[n].append({
                            'type': f'{"x_wing" if size == 2 else "swordfish"}_row',
                            'base_rows': list(rows),
                            'cover_cols': sorted(union_cols),
                            'candidate': k + 1,
                            'positions': base_positions,
                            'eliminations': eliminations,
                        })
            else:  # orientation == 'col'
                positions = [np.where(cand[:, c, k])[0] for c in range(9)]
                base_indices = [c for c in range(9) if 2 <= len(positions[c]) <= size]
                for cols in combinations(base_indices, size):
                    union_rows = set().union(*(set(positions[c]) for c in cols))
                    if len(union_rows) != size:
                        continue
                    base_positions = []
                    for c in cols:
                        for r in positions[c]:
                            base_positions.append((r, c))
                    eliminations = []
                    for r in sorted(union_rows):
                        for c in range(9):
                            if c in cols:
                                continue
                            if cand[r, c, k]:
                                eliminations.append(((r, c), [k + 1]))
                    if eliminations:
                        all_deductions[n].append({
                            'type': f'{"x_wing" if size == 2 else "swordfish"}_col',
                            'base_cols': list(cols),
                            'cover_rows': sorted(union_rows),
                            'candidate': k + 1,
                            'positions': base_positions,
                            'eliminations': eliminations,
                        })


def find_x_wing_rows(candidates: np.ndarray, all_deductions: list[list[dict]]):
    _find_fish(candidates, all_deductions, size=2, orientation='row')


def find_x_wing_cols(candidates: np.ndarray, all_deductions: list[list[dict]]):
    _find_fish(candidates, all_deductions, size=2, orientation='col')


def find_swordfish_rows(candidates: np.ndarray, all_deductions: list[list[dict]]):
    _find_fish(candidates, all_deductions, size=3, orientation='row')


def find_swordfish_cols(candidates: np.ndarray, all_deductions: list[list[dict]]):
    _find_fish(candidates, all_deductions, size=3, orientation='col')

