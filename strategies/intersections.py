# Intersections strategies: Locked Candidates (pointing and claiming)

import numpy as np

def find_locked_candidates_pointing(candidates: np.ndarray, all_deductions: list[list[dict]]):
    """
    Finds locked candidates (pointing): If a candidate in a box is confined to one row or col, eliminate it from the rest of that row/col outside the box.
    """
    N = candidates.shape[0]
    for n in range(N):
        for br in range(3):
            for bc in range(3):
                sub_cand = candidates[n, br*3:(br+1)*3, bc*3:(bc+1)*3, :]
                for k in range(9):
                    pos_mask = sub_cand[:, :, k]
                    if np.any(pos_mask):
                        rows_with = np.any(pos_mask, axis=1)
                        cols_with = np.any(pos_mask, axis=0)
                        if np.sum(rows_with) == 1:  # confined to one row in box
                            sr = np.where(rows_with)[0][0]
                            r = br*3 + sr
                            # Eliminate k+1 from rest of row outside box
                            box_cols = slice(bc*3, (bc+1)*3)
                            other_cols = [j for j in range(9) if not (bc*3 <= j < (bc+1)*3)]
                            elims = []
                            for j in other_cols:
                                if candidates[n, r, j, k]:
                                    elims.append(((r, j), [k+1]))
                            if elims:
                                all_deductions[n].append({
                                    'type': 'locked_pointing_row',
                                    'box': (br, bc),
                                    'value': k+1,
                                    'eliminations': elims
                                })
                        if np.sum(cols_with) == 1:  # confined to one col in box
                            sc = np.where(cols_with)[0][0]
                            c = bc*3 + sc
                            # Eliminate k+1 from rest of col outside box
                            box_rows = slice(br*3, (br+1)*3)
                            other_rows = [i for i in range(9) if not (br*3 <= i < (br+1)*3)]
                            elims = []
                            for i in other_rows:
                                if candidates[n, i, c, k]:
                                    elims.append(((i, c), [k+1]))
                            if elims:
                                all_deductions[n].append({
                                    'type': 'locked_pointing_col',
                                    'box': (br, bc),
                                    'value': k+1,
                                    'eliminations': elims
                                })

def find_locked_candidates_claiming(candidates: np.ndarray, all_deductions: list[list[dict]]):
    """
    Finds locked candidates (claiming): If a candidate in a row/col is confined to one box, eliminate it from the rest of that box.
    """
    N = candidates.shape[0]
    for n in range(N):
        # For rows
        for r in range(9):
            row_cand = candidates[n, r, :, :]
            for k in range(9):
                pos = np.where(row_cand[:, k])[0]
                if len(pos) > 0:
                    boxes = np.floor_divide(pos, 3)
                    if len(np.unique(boxes)) == 1:
                        bc = boxes[0]
                        # Eliminate k+1 from rest of box outside row
                        br = r // 3
                        box_rows = slice(br*3, (br+1)*3)
                        other_rows = [i for i in range(br*3, (br+1)*3) if i != r]
                        elims = []
                        for i in other_rows:
                            for j in range(bc*3, (bc+1)*3):
                                if candidates[n, i, j, k]:
                                    elims.append(((i, j), [k+1]))
                        if elims:
                            all_deductions[n].append({
                                'type': 'locked_claiming_row',
                                'row': r,
                                'value': k+1,
                                'eliminations': elims
                            })
        # For cols
        for c in range(9):
            col_cand = candidates[n, :, c, :]
            for k in range(9):
                pos = np.where(col_cand[:, k])[0]
                if len(pos) > 0:
                    boxes = np.floor_divide(pos, 3)
                    if len(np.unique(boxes)) == 1:
                        br = boxes[0]
                        # Eliminate k+1 from rest of box outside col
                        bc = c // 3
                        box_cols = slice(bc*3, (bc+1)*3)
                        other_cols = [j for j in range(bc*3, (bc+1)*3) if j != c]
                        elims = []
                        for j in other_cols:
                            for i in range(br*3, (br+1)*3):
                                if candidates[n, i, j, k]:
                                    elims.append(((i, j), [k+1]))
                        if elims:
                            all_deductions[n].append({
                                'type': 'locked_claiming_col',
                                'col': c,
                                'value': k+1,
                                'eliminations': elims
                            })
                            