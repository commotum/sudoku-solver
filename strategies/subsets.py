import numpy as np
from itertools import combinations


def _bitmask(arr: np.ndarray) -> np.ndarray:
    return arr.astype(int) @ (1 << np.arange(9))


def naked_subsets(lattice: np.ndarray, grid: np.ndarray, sizes=(2, 3, 4)) -> list[dict]:
    """Find naked pairs/triples/quads in rows, columns and boxes."""
    deductions: list[dict] = []
    for size in sizes:
        # Rows
        for r in range(9):
            unit = lattice[r]
            masks = _bitmask(unit)
            mask_map: dict[int, list[int]] = {}
            for c in range(9):
                if grid[r, c] != 0:
                    continue
                mask = int(masks[c])
                if mask == 0:
                    continue
                if mask.bit_count() == size:
                    mask_map.setdefault(mask, []).append(c)
            for mask, cols in mask_map.items():
                if len(cols) != size:
                    continue
                digits = [d + 1 for d in range(9) if mask >> d & 1]
                elims = []
                for c in range(9):
                    if c in cols or grid[r, c] != 0:
                        continue
                    rem = [v for v in digits if lattice[r, c, v - 1]]
                    if rem:
                        elims.append(((r, c), rem))
                if elims:
                    deductions.append({'type': f'naked_{size}_row',
                                       'positions': [(r, c) for c in cols],
                                       'values': digits,
                                       'eliminations': elims})
        # Columns
        for c in range(9):
            unit = lattice[:, c]
            masks = _bitmask(unit)
            mask_map: dict[int, list[int]] = {}
            for r in range(9):
                if grid[r, c] != 0:
                    continue
                mask = int(masks[r])
                if mask == 0:
                    continue
                if mask.bit_count() == size:
                    mask_map.setdefault(mask, []).append(r)
            for mask, rows in mask_map.items():
                if len(rows) != size:
                    continue
                digits = [d + 1 for d in range(9) if mask >> d & 1]
                elims = []
                for r in range(9):
                    if r in rows or grid[r, c] != 0:
                        continue
                    rem = [v for v in digits if lattice[r, c, v - 1]]
                    if rem:
                        elims.append(((r, c), rem))
                if elims:
                    deductions.append({'type': f'naked_{size}_col',
                                       'positions': [(r, c) for r in rows],
                                       'values': digits,
                                       'eliminations': elims})
        # Boxes
        for br in range(3):
            for bc in range(3):
                box = lattice[br*3:(br+1)*3, bc*3:(bc+1)*3]
                masks = _bitmask(box.reshape(9, 9))
                mask_map: dict[int, list[int]] = {}
                for idx in range(9):
                    r, c = divmod(idx, 3)
                    R, C = br*3 + r, bc*3 + c
                    if grid[R, C] != 0:
                        continue
                    mask = int(masks[idx])
                    if mask == 0:
                        continue
                    if mask.bit_count() == size:
                        mask_map.setdefault(mask, []).append(idx)
                for mask, idxs in mask_map.items():
                    if len(idxs) != size:
                        continue
                    digits = [d + 1 for d in range(9) if mask >> d & 1]
                    elims = []
                    for idx in range(9):
                        if idx in idxs:
                            continue
                        r, c = divmod(idx, 3)
                        R, C = br*3 + r, bc*3 + c
                        if grid[R, C] != 0:
                            continue
                        rem = [v for v in digits if lattice[R, C, v - 1]]
                        if rem:
                            elims.append(((R, C), rem))
                    if elims:
                        positions = []
                        for idx in idxs:
                            r, c = divmod(idx, 3)
                            positions.append((br*3 + r, bc*3 + c))
                        deductions.append({'type': f'naked_{size}_box',
                                           'positions': positions,
                                           'values': digits,
                                           'eliminations': elims})
    return deductions


def hidden_subsets(lattice: np.ndarray, grid: np.ndarray, sizes=(2, 3, 4)) -> list[dict]:
    """Find hidden pairs/triples/quads in rows, columns and boxes."""
    deductions: list[dict] = []
    nums = np.arange(9)
    for size in sizes:
        # Rows
        for r in range(9):
            unit = lattice[r]
            cand_cells = [set(np.where(unit[:, k])[0]) for k in range(9)]
            for comb in combinations(nums, size):
                pos = set.union(*(cand_cells[k] for k in comb))
                if len(pos) != size:
                    continue
                elims = []
                for c in pos:
                    other = [v + 1 for v in nums if v not in comb and lattice[r, c, v]]
                    if other:
                        elims.append(((r, int(c)), other))
                if elims:
                    positions = [(r, int(c)) for c in pos]
                    digits = [int(k + 1) for k in comb]
                    deductions.append({'type': f'hidden_{size}_row',
                                       'positions': positions,
                                       'values': digits,
                                       'eliminations': elims})
        # Columns
        for c in range(9):
            unit = lattice[:, c]
            cand_cells = [set(np.where(unit[:, k])[0]) for k in range(9)]
            for comb in combinations(nums, size):
                pos = set.union(*(cand_cells[k] for k in comb))
                if len(pos) != size:
                    continue
                elims = []
                for r in pos:
                    other = [v + 1 for v in nums if v not in comb and lattice[r, c, v]]
                    if other:
                        elims.append(((int(r), c), other))
                if elims:
                    positions = [(int(r), c) for r in pos]
                    digits = [int(k + 1) for k in comb]
                    deductions.append({'type': f'hidden_{size}_col',
                                       'positions': positions,
                                       'values': digits,
                                       'eliminations': elims})
        # Boxes
        for br in range(3):
            for bc in range(3):
                box = lattice[br*3:(br+1)*3, bc*3:(bc+1)*3]
                cand_cells = [set(np.where(box.reshape(9, 9)[:, k])[0]) for k in range(9)]
                for comb in combinations(nums, size):
                    pos = set.union(*(cand_cells[k] for k in comb))
                    if len(pos) != size:
                        continue
                    elims = []
                    positions = []
                    for idx in pos:
                        r, c = divmod(idx, 3)
                        R, C = br*3 + r, bc*3 + c
                        other = [v + 1 for v in nums if v not in comb and lattice[R, C, v]]
                        if other:
                            elims.append(((R, C), other))
                        positions.append((R, C))
                    if elims:
                        digits = [int(k + 1) for k in comb]
                        deductions.append({'type': f'hidden_{size}_box',
                                           'positions': positions,
                                           'values': digits,
                                           'eliminations': elims})
    return deductions
