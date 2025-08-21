from pathlib import Path
import os
import re
import random

import numpy as np

# Precompute houses
ROWS = [[(r, c) for c in range(9)] for r in range(9)]
COLS = [[(r, c) for r in range(9)] for c in range(9)]
BLOCKS = [
    [
        (r, c)
        for r in range(br * 3, br * 3 + 3)
        for c in range(bc * 3, bc * 3 + 3)
    ]
    for br in range(3)
    for bc in range(3)
]
HOUSES = ROWS + COLS + BLOCKS

# Peers for assignments
PEERS = [[set() for _ in range(9)] for _ in range(9)]
for r in range(9):
    for c in range(9):
        peers = set(ROWS[r] + COLS[c] + BLOCKS[(r // 3) * 3 + (c // 3)])
        peers.remove((r, c))
        PEERS[r][c] = peers


def digits_from_cand(cand_rc: np.ndarray) -> list[int]:
    """Return list of 1-based digits present in a candidate boolean slice."""
    return [d + 1 for d in range(9) if cand_rc[d]]


def candidate_mask_init(grids: np.ndarray) -> np.ndarray:
    """Compute boolean candidate masks for a batch of grids."""
    if grids.ndim == 2:
        grids = grids[None, ...]
    N = grids.shape[0]
    mask = np.ones((N, 9, 9, 9), dtype=bool)
    for n in range(N):
        grid = grids[n]
        for r in range(9):
            for c in range(9):
                val = int(grid[r, c])
                if val:
                    d = val - 1
                    mask[n, r, c, :] = False
                    mask[n, r, c, d] = True
                    mask[n, r, :, d] = False
                    mask[n, :, c, d] = False
                    br, bc = r // 3, c // 3
                    mask[n, br * 3 : br * 3 + 3, bc * 3 : bc * 3 + 3, d] = False
                    mask[n, r, c, d] = True
    return mask


def assign(grid: np.ndarray, mask: np.ndarray, r: int, c: int, d0idx: int) -> None:
    """Assign digit index ``d0idx`` (0-based) to cell ``(r, c)`` updating peers."""
    grid[r, c] = d0idx + 1
    mask[r, c, :] = False
    mask[r, c, d0idx] = True
    mask[r, :, d0idx] = False
    mask[:, c, d0idx] = False
    br, bc = r // 3, c // 3
    mask[br * 3 : br * 3 + 3, bc * 3 : bc * 3 + 3, d0idx] = False
    mask[r, c, d0idx] = True


def apply_deductions(
    grids: np.ndarray, mask: np.ndarray, all_deductions: list[list[dict]]
) -> int:
    """Apply recorded deductions to grids and masks in-place."""
    if grids.ndim == 2:
        grids = grids[None, ...]
        mask = mask[None, ...]
    changes = 0
    for n, deds in enumerate(all_deductions):
        for ded in deds:
            if "value" in ded and "position" in ded:
                r, c = ded["position"]
                d = ded["value"] - 1
                if grids[n, r, c] == 0:
                    assign(grids[n], mask[n], r, c, d)
                    changes += 1
            if "eliminations" in ded:
                for (r, c), vals in ded["eliminations"]:
                    for val in vals:
                        d = val - 1
                        if mask[n, r, c, d]:
                            mask[n, r, c, d] = False
                            changes += 1
    return changes


def is_solved(grids: np.ndarray) -> np.ndarray:
    """Check whether each puzzle in the batch is completely filled."""
    arr = grids if grids.ndim == 3 else grids[None, ...]
    return np.all(arr != 0, axis=(1, 2))


def is_valid(grids: np.ndarray) -> np.ndarray:
    """Validate each puzzle: no duplicates in rows, columns or boxes (ignoring zeros)."""
    N = grids.shape[0]
    valid = np.ones(N, dtype=bool)

    # Check rows
    for i in range(9):
        row_vals = grids[:, i, :]
        for n in range(N):
            if not valid[n]:
                continue
            non_zero = row_vals[n][row_vals[n] != 0]
            if len(non_zero) != len(np.unique(non_zero)):
                valid[n] = False

    # Check columns
    for j in range(9):
        col_vals = grids[:, :, j]
        for n in range(N):
            if not valid[n]:
                continue
            non_zero = col_vals[n][col_vals[n] != 0]
            if len(non_zero) != len(np.unique(non_zero)):
                valid[n] = False

    # Check boxes
    for br in range(3):
        for bc in range(3):
            subgrids = grids[:, br*3:(br+1)*3, bc*3:(bc+1)*3]
            for n in range(N):
                if not valid[n]:
                    continue
                flat = subgrids[n].flatten()
                non_zero = flat[flat != 0]
                if len(non_zero) != len(np.unique(non_zero)):
                    valid[n] = False

    return valid


def repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    """Return the base data directory.

    Default location is ``repo_root()/"data"/"sudoku-extreme-processed"``.
    The ``SUDOKU_DATA_DIR`` environment variable can override it.
    """
    default = repo_root() / "data" / "sudoku-extreme-processed"
    return Path(os.environ.get("SUDOKU_DATA_DIR", default))


def available_levels() -> list[int]:
    """Discover available integer levels from the data layout."""
    base = data_dir()
    levels: set[int] = set()
    for p in base.glob("lvl-*-inputs.npy"):
        m = re.search(r"lvl-(\d+)-inputs\.npy", p.name)
        if m:
            levels.add(int(m.group(1)))
    return sorted(levels)


def is_valid_level(level: int) -> bool:
    """Return ``True`` if ``level`` is a non-negative integer and exists."""
    return level >= 0 and level in set(available_levels())


def random_level() -> int:
    """Return a random available level."""
    levels = available_levels()
    if not levels:
        raise RuntimeError("No levels available in data directory")
    return random.choice(levels)

