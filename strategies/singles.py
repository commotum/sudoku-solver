import numpy as np


def naked_single(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    """Return fills for cells with only one candidate."""
    fills: list[dict] = []
    counts = lattice.sum(axis=2)
    for r, c in np.argwhere((counts == 1) & (grid == 0)):
        v = int(np.argmax(lattice[r, c]) + 1)
        fills.append({'type': 'naked_single', 'position': (int(r), int(c)), 'value': v})
    return fills


def hidden_single(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    """Return fills where a candidate is unique in a unit."""
    fills: list[dict] = []
    # Rows
    for r in range(9):
        row = lattice[r]
        counts = row.sum(axis=0)
        for k in np.where(counts == 1)[0]:
            c = int(np.argmax(row[:, k]))
            if grid[r, c] == 0:
                fills.append({'type': 'hidden_single_row', 'position': (r, c), 'value': int(k + 1)})
    # Columns
    for c in range(9):
        col = lattice[:, c]
        counts = col.sum(axis=0)
        for k in np.where(counts == 1)[0]:
            r = int(np.argmax(col[:, k]))
            if grid[r, c] == 0:
                fills.append({'type': 'hidden_single_col', 'position': (r, c), 'value': int(k + 1)})
    # Boxes
    for br in range(3):
        for bc in range(3):
            box = lattice[br*3:(br+1)*3, bc*3:(bc+1)*3, :]
            counts = box.sum(axis=(0, 1))
            for k in np.where(counts == 1)[0]:
                sr, sc = np.argwhere(box[:, :, k])[0]
                r, c = br*3 + int(sr), bc*3 + int(sc)
                if grid[r, c] == 0:
                    fills.append({'type': 'hidden_single_box', 'position': (r, c), 'value': int(k + 1)})
    return fills
