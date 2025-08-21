"""Single-digit deduction strategies using boolean candidate grids."""

import numpy as np

from engine.utils import ROWS, COLS, BLOCKS


def find_naked_singles(mask: np.ndarray, out: list[list[dict]]) -> None:
    """Identify cells that have only one remaining candidate."""
    pcs = mask.sum(axis=3)
    N = mask.shape[0]
    for n in range(N):
        rs, cs = np.where(pcs[n] == 1)
        for r, c in zip(rs, cs):
            digit = int(np.where(mask[n, r, c])[0][0] + 1)
            out[n].append({"type": "naked_single", "position": (r, c), "value": digit})


def _hidden_single(mask: np.ndarray, houses: list[list[tuple[int, int]]], tag: str, out: list[list[dict]]) -> None:
    """Common helper for hidden singles across ``houses`` with result ``tag``."""
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for H in houses:
            cells = np.array([m[r, c] for r, c in H])
            for digit in range(9):
                positions = np.where(cells[:, digit])[0]
                if len(positions) == 1:
                    idx = positions[0]
                    r, c = H[idx]
                    out[n].append({"type": tag, "position": (r, c), "value": digit + 1})


def find_hidden_singles_rows(mask: np.ndarray, out: list[list[dict]]) -> None:
    _hidden_single(mask, ROWS, "hidden_single_row", out)


def find_hidden_singles_cols(mask: np.ndarray, out: list[list[dict]]) -> None:
    _hidden_single(mask, COLS, "hidden_single_col", out)


def find_hidden_singles_boxes(mask: np.ndarray, out: list[list[dict]]) -> None:
    _hidden_single(mask, BLOCKS, "hidden_single_box", out)

