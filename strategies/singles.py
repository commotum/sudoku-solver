# Singles strategies: Naked Single, Hidden Single (row/col/box)

import numpy as np

def find_naked_singles(candidates: np.ndarray, all_deductions: list[list[dict]]):
    N = candidates.shape[0]
    cell_counts = np.sum(candidates, axis=3)  # (N, 9, 9)
    naked_mask = (cell_counts == 1)
    for n in range(N):
        positions = np.argwhere(naked_mask[n])
        for i, j in positions:
            k = np.where(candidates[n, i, j])[0][0]
            all_deductions[n].append({
                'type': 'naked_single',
                'position': (i, j),
                'value': k + 1
            })

def find_hidden_singles_rows(candidates: np.ndarray, all_deductions: list[list[dict]]):
    N = candidates.shape[0]
    row_counts = np.sum(candidates, axis=2)  # (N, 9 rows, 9 nums)
    row_hidden_mask = (row_counts == 1)
    for n in range(N):
        for r in range(9):
            for k in range(9):
                if row_hidden_mask[n, r, k]:
                    j = np.where(candidates[n, r, :, k])[0][0]
                    all_deductions[n].append({
                        'type': 'hidden_single_row',
                        'position': (r, j),
                        'value': k + 1
                    })

def find_hidden_singles_cols(candidates: np.ndarray, all_deductions: list[list[dict]]):
    N = candidates.shape[0]
    col_counts = np.sum(candidates, axis=1)  # (N, 9 cols, 9 nums)
    col_hidden_mask = (col_counts == 1)
    for n in range(N):
        for c in range(9):
            for k in range(9):
                if col_hidden_mask[n, c, k]:
                    i = np.where(candidates[n, :, c, k])[0][0]
                    all_deductions[n].append({
                        'type': 'hidden_single_col',
                        'position': (i, c),
                        'value': k + 1
                    })

def find_hidden_singles_boxes(candidates: np.ndarray, all_deductions: list[list[dict]]):
    N = candidates.shape[0]
    for br in range(3):
        for bc in range(3):
            sub_cand = candidates[:, br*3:(br+1)*3, bc*3:(bc+1)*3, :]
            box_counts = np.sum(sub_cand, axis=(1, 2))  # (N, 9 nums)
            box_hidden_mask = (box_counts == 1)
            for n in range(N):
                for k in range(9):
                    if box_hidden_mask[n, k]:
                        pos = np.argwhere(sub_cand[n, :, :, k])
                        sr, sc = pos[0, 0], pos[0, 1]
                        i, j = br*3 + sr, bc*3 + sc
                        all_deductions[n].append({
                            'type': 'hidden_single_box',
                            'position': (i, j),
                            'value': k + 1
                        })