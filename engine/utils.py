# Helpers: Grid validation, apply_deduction, candidate computation

from pathlib import Path
import os
import re
import random

import numpy as np


def compute_candidates(grids: np.ndarray) -> np.ndarray:
    """Compute candidate masks for a batch of grids.

    Args:
        grids: np.ndarray of shape (N, 9, 9) with values 0-9.

    Returns:
        np.ndarray of shape (N, 9, 9, 9) where the last dimension is a
        boolean mask for candidate values 1-9.
    """
    if grids.shape[1:] != (9, 9):
        raise ValueError("Grids must be (N, 9, 9)")

    N = grids.shape[0]

    row_forbidden = np.stack(
        [np.any(grids == k, axis=2) for k in range(1, 10)], axis=-1
    )  # (N, 9, 9 nums)
    col_forbidden = np.stack(
        [np.any(grids == k, axis=1) for k in range(1, 10)], axis=-1
    )  # (N, 9, 9 nums)

    box_forbidden = np.zeros((N, 9, 9), dtype=bool)
    for br in range(3):
        for bc in range(3):
            subgrid = grids[:, br * 3 : (br + 1) * 3, bc * 3 : (bc + 1) * 3]
            box_idx = br * 3 + bc
            for k in range(1, 10):
                box_forbidden[:, box_idx, k - 1] = np.any(subgrid == k, axis=(1, 2))

    empty = grids == 0
    candidates = np.tile(empty[:, :, :, None], (1, 1, 1, 9))
    candidates &= ~row_forbidden[:, :, None, :]
    candidates &= ~col_forbidden[:, None, :, :]

    row_to_box = np.floor_divide(np.arange(9), 3)
    box_idx = row_to_box[:, None] * 3 + row_to_box[None, :]
    box_forbidden_per_cell = box_forbidden[:, box_idx, :]
    candidates &= ~box_forbidden_per_cell

    return candidates


def is_solved(grids: np.ndarray) -> np.ndarray:
    """
    Checks if each puzzle in the batch is fully solved (all cells filled with 1-9, no zeros).
    
    Args:
        grids: np.ndarray of shape (N, 9, 9).
    
    Returns:
        np.ndarray of shape (N,) with bools: True if solved.
    """
    return np.all(grids != 0, axis=(1, 2))

def is_valid(grids: np.ndarray) -> np.ndarray:
    """
    Validates each puzzle in the batch: No duplicates in rows, columns, or boxes (ignoring zeros).
    
    Args:
        grids: np.ndarray of shape (N, 9, 9).
    
    Returns:
        np.ndarray of shape (N,) with bools: True if valid (no conflicts).
    """
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

def apply_deductions(
    grids: np.ndarray, candidates: np.ndarray, all_deductions: list[list[dict]]
) -> int:
    """Apply fills and eliminations to grids and candidates in-place.

    Args:
        grids: np.ndarray of shape (N, 9, 9) to modify.
        candidates: np.ndarray of shape (N, 9, 9, 9) to modify.
        all_deductions: List of deductions per puzzle.

    Returns:
        Total number of changes (fills + eliminations) applied.
    """

    N = grids.shape[0]
    applied_count = 0

    for n in range(N):
        for ded in all_deductions[n]:
            if 'value' in ded and 'position' in ded:
                i, j = ded['position']
                val = ded['value']
                if grids[n, i, j] == 0:
                    grids[n, i, j] = val
                    applied_count += 1
                    candidates[n, i, j, :] = False
                    candidates[n, i, :, val - 1] = False
                    candidates[n, :, j, val - 1] = False
                    br, bc = i // 3, j // 3
                    candidates[
                        n,
                        br * 3 : (br + 1) * 3,
                        bc * 3 : (bc + 1) * 3,
                        val - 1,
                    ] = False
            if 'eliminations' in ded:
                for (i, j), vals in ded['eliminations']:
                    for val in vals:
                        if candidates[n, i, j, val - 1]:
                            candidates[n, i, j, val - 1] = False
                            applied_count += 1

    return applied_count


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
