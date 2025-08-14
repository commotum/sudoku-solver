import numpy as np


def locked_candidates_pointing(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    """Pointing triples: candidate confined to a single row/col within a box."""
    deductions: list[dict] = []
    for br in range(3):
        for bc in range(3):
            box = lattice[br*3:(br+1)*3, bc*3:(bc+1)*3]
            for k in range(9):
                positions = np.argwhere(box[:, :, k])
                if len(positions) <= 1:
                    continue
                rows = np.unique(positions[:, 0])
                cols = np.unique(positions[:, 1])
                if len(rows) == 1:
                    r = br*3 + rows[0]
                    cols_global = bc*3 + positions[:, 1]
                    elims = []
                    for c in set(range(9)) - set(cols_global):
                        if lattice[r, c, k]:
                            elims.append(((r, c), [k + 1]))
                    if elims:
                        deductions.append({'type': 'locked_pointing_row',
                                           'box': (br, bc),
                                           'value': k + 1,
                                           'eliminations': elims})
                if len(cols) == 1:
                    c = bc*3 + cols[0]
                    rows_global = br*3 + positions[:, 0]
                    elims = []
                    for r in set(range(9)) - set(rows_global):
                        if lattice[r, c, k]:
                            elims.append(((r, c), [k + 1]))
                    if elims:
                        deductions.append({'type': 'locked_pointing_col',
                                           'box': (br, bc),
                                           'value': k + 1,
                                           'eliminations': elims})
    return deductions


def locked_candidates_claiming(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    """Claiming: candidates confined to single box within a row/column."""
    deductions: list[dict] = []
    # Rows
    for r in range(9):
        row = lattice[r]
        for k in range(9):
            cols = np.where(row[:, k])[0]
            if len(cols) <= 1:
                continue
            boxes = np.unique(cols // 3)
            if len(boxes) == 1:
                bc = boxes[0]
                elims = []
                for c in range(bc*3, bc*3 + 3):
                    if c in cols:
                        continue
                    if lattice[r, c, k]:
                        elims.append(((r, c), [k + 1]))
                if elims:
                    deductions.append({'type': 'locked_claiming_row',
                                       'row': r,
                                       'value': k + 1,
                                       'eliminations': elims})
    # Columns
    for c in range(9):
        col = lattice[:, c]
        for k in range(9):
            rows = np.where(col[:, k])[0]
            if len(rows) <= 1:
                continue
            boxes = np.unique(rows // 3)
            if len(boxes) == 1:
                br = boxes[0]
                elims = []
                for r in range(br*3, br*3 + 3):
                    if r in rows:
                        continue
                    if lattice[r, c, k]:
                        elims.append(((r, c), [k + 1]))
                if elims:
                    deductions.append({'type': 'locked_claiming_col',
                                       'col': c,
                                       'value': k + 1,
                                       'eliminations': elims})
    return deductions
