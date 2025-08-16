# Subsets strategies: Naked/Hidden Pairs/Triplets/Quads (row/col/box variants)

import numpy as np
from itertools import combinations

def find_naked_subsets(candidates: np.ndarray, all_deductions: list[list[dict]], sizes: list[int] = [2, 3, 4], units: list[str] = ['row', 'col', 'box']):
    """
    Finds naked subsets (pairs, triplets, quads) in specified units.
    A naked subset is a group of k cells in a unit that together have exactly k candidates.
    Eliminates those candidates from other cells in the unit.
    """
    N = candidates.shape[0]
    for size in sizes:
        for unit_type in units:
            if unit_type == 'row':
                for n in range(N):
                    for r in range(9):
                        unit_cand = candidates[n, r, :, :]
                        empty_cells = np.where(np.any(unit_cand, axis=1))[0]  # indices of cells with candidates
                        if len(empty_cells) < size:
                            continue
                        for cell_comb in combinations(empty_cells, size):
                            subset_cand = unit_cand[list(cell_comb), :]
                            union = np.any(subset_cand, axis=0)
                            if np.sum(union) == size:
                                # Valid naked subset
                                elim_vals = np.where(union)[0] + 1
                                other_cells = [j for j in range(9) if j not in cell_comb]
                                elims = []
                                for j in other_cells:
                                    cell_elim = np.where(unit_cand[j] & union)[0] + 1
                                    if len(cell_elim) > 0:
                                        elims.append(((r, j), list(cell_elim)))
                                if elims:
                                    all_deductions[n].append({
                                        'type': f'naked_{size}_{unit_type}',
                                        'positions': [(r, j) for j in cell_comb],
                                        'values': list(elim_vals),
                                        'eliminations': elims
                                    })
            elif unit_type == 'col':
                for n in range(N):
                    for c in range(9):
                        unit_cand = candidates[n, :, c, :]
                        empty_cells = np.where(np.any(unit_cand, axis=1))[0]
                        if len(empty_cells) < size:
                            continue
                        for cell_comb in combinations(empty_cells, size):
                            subset_cand = unit_cand[list(cell_comb), :]
                            union = np.any(subset_cand, axis=0)
                            if np.sum(union) == size:
                                elim_vals = np.where(union)[0] + 1
                                other_cells = [i for i in range(9) if i not in cell_comb]
                                elims = []
                                for i in other_cells:
                                    cell_elim = np.where(unit_cand[i] & union)[0] + 1
                                    if len(cell_elim) > 0:
                                        elims.append(((i, c), list(cell_elim)))
                                if elims:
                                    all_deductions[n].append({
                                        'type': f'naked_{size}_{unit_type}',
                                        'positions': [(i, c) for i in cell_comb],
                                        'values': list(elim_vals),
                                        'eliminations': elims
                                    })
            elif unit_type == 'box':
                for n in range(N):
                    for br in range(3):
                        for bc in range(3):
                            sub_cand = candidates[n, br*3:(br+1)*3, bc*3:(bc+1)*3, :]
                            flat_cand = sub_cand.reshape(9, 9)
                            empty_cells = np.where(np.any(flat_cand, axis=1))[0]
                            if len(empty_cells) < size:
                                continue
                            for cell_comb in combinations(empty_cells, size):
                                subset_cand = flat_cand[list(cell_comb), :]
                                union = np.any(subset_cand, axis=0)
                                if np.sum(union) == size:
                                    elim_vals = np.where(union)[0] + 1
                                    other_cells = [idx for idx in range(9) if idx not in cell_comb]
                                    elims = []
                                    for idx in other_cells:
                                        sr, sc = divmod(idx, 3)
                                        i, j = br*3 + sr, bc*3 + sc
                                        cell_elim = np.where(flat_cand[idx] & union)[0] + 1
                                        if len(cell_elim) > 0:
                                            elims.append(((i, j), list(cell_elim)))
                                    if elims:
                                        all_deductions[n].append({
                                            'type': f'naked_{size}_{unit_type}',
                                            'positions': [(br*3 + divmod(idx, 3)[0], bc*3 + divmod(idx, 3)[1]) for idx in cell_comb],
                                            'values': list(elim_vals),
                                            'eliminations': elims
                                        })

def find_hidden_subsets(candidates: np.ndarray, all_deductions: list[list[dict]], sizes: list[int] = [2, 3, 4], units: list[str] = ['row', 'col', 'box']):
    """
    Finds hidden subsets in specified units.
    A hidden subset is a group of k candidates that appear only in exactly k cells in the unit.
    Eliminates other candidates from those cells.
    """
    N = candidates.shape[0]
    for size in sizes:
        for unit_type in units:
            if unit_type == 'row':
                for n in range(N):
                    for r in range(9):
                        unit_cand = candidates[n, r, :, :]
                        cand_counts = np.sum(unit_cand, axis=0)  # count per num
                        low_freq_cands = np.where((cand_counts > 0) & (cand_counts <= size))[0]
                        if len(low_freq_cands) < size:
                            continue
                        for cand_comb in combinations(low_freq_cands, size):
                            positions = [np.where(unit_cand[:, k])[0] for k in cand_comb]
                            union_pos = np.unique(np.concatenate(positions))
                            if len(union_pos) == size:
                                # Valid hidden subset
                                vals = list(np.array(cand_comb) + 1)
                                pos_list = [(r, int(j)) for j in union_pos]
                                elims = []
                                for j in union_pos:
                                    other_cands = np.where(unit_cand[j] & ~np.isin(np.arange(9), cand_comb))[0] + 1
                                    if len(other_cands) > 0:
                                        elims.append(((r, int(j)), list(other_cands)))
                                if elims:
                                    all_deductions[n].append({
                                        'type': f'hidden_{size}_{unit_type}',
                                        'positions': pos_list,
                                        'values': vals,
                                        'eliminations': elims
                                    })
            elif unit_type == 'col':
                for n in range(N):
                    for c in range(9):
                        unit_cand = candidates[n, :, c, :]
                        cand_counts = np.sum(unit_cand, axis=0)
                        low_freq_cands = np.where((cand_counts > 0) & (cand_counts <= size))[0]
                        if len(low_freq_cands) < size:
                            continue
                        for cand_comb in combinations(low_freq_cands, size):
                            positions = [np.where(unit_cand[:, k])[0] for k in cand_comb]
                            union_pos = np.unique(np.concatenate(positions))
                            if len(union_pos) == size:
                                vals = list(np.array(cand_comb) + 1)
                                pos_list = [(int(i), c) for i in union_pos]
                                elims = []
                                for i in union_pos:
                                    other_cands = np.where(unit_cand[i] & ~np.isin(np.arange(9), cand_comb))[0] + 1
                                    if len(other_cands) > 0:
                                        elims.append(((int(i), c), list(other_cands)))
                                if elims:
                                    all_deductions[n].append({
                                        'type': f'hidden_{size}_{unit_type}',
                                        'positions': pos_list,
                                        'values': vals,
                                        'eliminations': elims
                                    })
            elif unit_type == 'box':
                for n in range(N):
                    for br in range(3):
                        for bc in range(3):
                            sub_cand = candidates[n, br*3:(br+1)*3, bc*3:(bc+1)*3, :]
                            flat_cand = sub_cand.reshape(9, 9)
                            cand_counts = np.sum(flat_cand, axis=0)
                            low_freq_cands = np.where((cand_counts > 0) & (cand_counts <= size))[0]
                            if len(low_freq_cands) < size:
                                continue
                            for cand_comb in combinations(low_freq_cands, size):
                                positions = [np.where(flat_cand[:, k])[0] for k in cand_comb]
                                union_pos = np.unique(np.concatenate(positions))
                                if len(union_pos) == size:
                                    vals = list(np.array(cand_comb) + 1)
                                    pos_list = []
                                    for idx in union_pos:
                                        sr, sc = divmod(idx, 3)
                                        i, j = br*3 + sr, bc*3 + sc
                                        pos_list.append((i, j))
                                    elims = []
                                    for idx in union_pos:
                                        sr, sc = divmod(idx, 3)
                                        i, j = br*3 + sr, bc*3 + sc
                                        other_cands = np.where(flat_cand[idx] & ~np.isin(np.arange(9), cand_comb))[0] + 1
                                        if len(other_cands) > 0:
                                            elims.append(((i, j), list(other_cands)))
                                    if elims:
                                        all_deductions[n].append({
                                            'type': f'hidden_{size}_{unit_type}',
                                            'positions': pos_list,
                                            'values': vals,
                                            'eliminations': elims
                                        })