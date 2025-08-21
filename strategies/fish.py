"""Fish pattern strategies implemented on boolean candidate grids."""

from itertools import combinations
import numpy as np


def _fish(mask: np.ndarray, size: int, orient: str, name: str, out: list[list[dict]]):
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for digit in range(1, 10):
            d = digit - 1
            if orient == "row":
                sets = [{c for c in range(9) if m[r, c, d]} for r in range(9)]
                for rows in combinations(range(9), size):
                    cols_union = set().union(*(sets[r] for r in rows))
                    if len(cols_union) != size:
                        continue
                    if any(not sets[r] or not sets[r].issubset(cols_union) for r in rows):
                        continue
                    elims: dict[tuple[int, int], list[int]] = {}
                    for rr in range(9):
                        if rr in rows:
                            continue
                        for c in cols_union:
                            if m[rr, c, d]:
                                elims.setdefault((rr, c), []).append(digit)
                    if elims:
                        out[n].append({
                            "type": f"{name}_row",
                            "base": rows,
                            "eliminations": list(elims.items()),
                        })
            else:
                sets = [{r for r in range(9) if m[r, c, d]} for c in range(9)]
                for cols in combinations(range(9), size):
                    rows_union = set().union(*(sets[c] for c in cols))
                    if len(rows_union) != size:
                        continue
                    if any(not sets[c] or not sets[c].issubset(rows_union) for c in cols):
                        continue
                    elims: dict[tuple[int, int], list[int]] = {}
                    for cc in range(9):
                        if cc in cols:
                            continue
                        for r in rows_union:
                            if m[r, cc, d]:
                                elims.setdefault((r, cc), []).append(digit)
                    if elims:
                        out[n].append({
                            "type": f"{name}_col",
                            "base": cols,
                            "eliminations": list(elims.items()),
                        })


def find_x_wing_rows(mask: np.ndarray, out: list[list[dict]]) -> None:
    _fish(mask, 2, "row", "x_wing", out)


def find_x_wing_cols(mask: np.ndarray, out: list[list[dict]]) -> None:
    _fish(mask, 2, "col", "x_wing", out)


def find_swordfish_rows(mask: np.ndarray, out: list[list[dict]]) -> None:
    _fish(mask, 3, "row", "swordfish", out)


def find_swordfish_cols(mask: np.ndarray, out: list[list[dict]]) -> None:
    _fish(mask, 3, "col", "swordfish", out)


def find_jellyfish_rows(mask: np.ndarray, out: list[list[dict]]) -> None:
    _fish(mask, 4, "row", "jellyfish", out)


def find_jellyfish_cols(mask: np.ndarray, out: list[list[dict]]) -> None:
    _fish(mask, 4, "col", "jellyfish", out)

