import numpy as np

from utils import popcount16, digits_from_mask, ROWS, COLS, BLOCKS, Pos


def find_naked_singles(mask: np.ndarray, out: list[list[dict]]) -> None:
    pcs = popcount16(mask)
    N = mask.shape[0]
    for n in range(N):
        rs, cs = np.where(pcs[n] == 1)
        for r, c in zip(rs, cs):
            digit = digits_from_mask(int(mask[n, r, c]))[0]
            out[n].append({"type": "naked_single", "position": (r, c), "value": digit})


def _hidden_single(mask: np.ndarray, houses: list[list[tuple[int, int]]], tag: str, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for H in houses:
            for digit in range(1, 10):
                pos = Pos(m, H, digit)
                if len(pos) == 1:
                    r, c = pos[0]
                    out[n].append({"type": tag, "position": (r, c), "value": digit})


def find_hidden_singles_rows(mask: np.ndarray, out: list[list[dict]]) -> None:
    _hidden_single(mask, ROWS, "hidden_single_row", out)


def find_hidden_singles_cols(mask: np.ndarray, out: list[list[dict]]) -> None:
    _hidden_single(mask, COLS, "hidden_single_col", out)


def find_hidden_singles_boxes(mask: np.ndarray, out: list[list[dict]]) -> None:
    _hidden_single(mask, BLOCKS, "hidden_single_box", out)
