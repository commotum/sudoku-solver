"""Uniqueness strategies implemented with boolean candidate grids."""

import numpy as np

from engine.utils import BLOCKS


def find_ur_type1(mask: np.ndarray, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for r1 in range(8):
            for r2 in range(r1 + 1, 9):
                for c1 in range(8):
                    for c2 in range(c1 + 1, 9):
                        cells = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
                        arrs = [m[r, c] for r, c in cells]
                        pairs: dict[tuple[int, int], list[int]] = {}
                        for idx, arr in enumerate(arrs):
                            digits = np.where(arr)[0]
                            if digits.size == 2:
                                pairs.setdefault(tuple(digits), []).append(idx)
                        for digits, idxs in pairs.items():
                            if len(idxs) == 3:
                                x0 = (set(range(4)) - set(idxs)).pop()
                                arr = arrs[x0]
                                if arr[list(digits)].all():
                                    extra = [d for d in np.where(arr)[0] if d not in digits]
                                    if len(extra) == 1:
                                        r, c = cells[x0]
                                        out[n].append({
                                            "type": "ur_type1",
                                            "position": (r, c),
                                            "value": int(extra[0] + 1),
                                        })


def _ur2_patterns(m: np.ndarray):
    """Yield UR2 pattern descriptions within mask ``m``.

    Each yielded dict contains:
        orientation: 'row' or 'col'
        floor: list of two (r, c) tuples for the floor cells
        extra: 0-based digit index locked in the floor
        block: block index if the floor is within a single block, else ``None``
    """
    for r1 in range(8):
        for r2 in range(r1 + 1, 9):
            for c1 in range(8):
                for c2 in range(c1 + 1, 9):
                    x11, x12, x21, x22 = (
                        m[r1, c1],
                        m[r1, c2],
                        m[r2, c1],
                        m[r2, c2],
                    )
                    # Horizontal floor at row r2
                    roof = [x11, x12]
                    floor = [x21, x22]
                    rd0, rd1 = np.where(roof[0])[0], np.where(roof[1])[0]
                    if rd0.size == 2 and np.array_equal(rd0, rd1):
                        fd0, fd1 = np.where(floor[0])[0], np.where(floor[1])[0]
                        if (
                            fd0.size == 3
                            and fd1.size == 3
                            and set(rd0).issubset(fd0)
                            and set(rd0).issubset(fd1)
                        ):
                            extra0 = list(set(fd0) - set(rd0))
                            extra1 = list(set(fd1) - set(rd0))
                            if extra0 and extra1 and extra0[0] == extra1[0]:
                                extra = extra0[0]
                                block = None
                                if c1 // 3 == c2 // 3:
                                    block = (r2 // 3) * 3 + (c1 // 3)
                                yield {
                                    "orientation": "row",
                                    "floor": [(r2, c1), (r2, c2)],
                                    "extra": extra,
                                    "block": block,
                                }
                    # Vertical floor at column c2
                    roof = [x11, x21]
                    floor = [x12, x22]
                    rd0, rd1 = np.where(roof[0])[0], np.where(roof[1])[0]
                    if rd0.size == 2 and np.array_equal(rd0, rd1):
                        fd0, fd1 = np.where(floor[0])[0], np.where(floor[1])[0]
                        if (
                            fd0.size == 3
                            and fd1.size == 3
                            and set(rd0).issubset(fd0)
                            and set(rd0).issubset(fd1)
                        ):
                            extra0 = list(set(fd0) - set(rd0))
                            extra1 = list(set(fd1) - set(rd0))
                            if extra0 and extra1 and extra0[0] == extra1[0]:
                                extra = extra0[0]
                                block = None
                                if r1 // 3 == r2 // 3:
                                    block = (r1 // 3) * 3 + (c2 // 3)
                                yield {
                                    "orientation": "col",
                                    "floor": [(r1, c2), (r2, c2)],
                                    "extra": extra,
                                    "block": block,
                                }


def find_ur_type2(mask: np.ndarray, out: list[list[dict]]) -> None:
    """UR Type 2: line-locked common extra digit."""
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for pat in _ur2_patterns(m):
            digit = pat["extra"]
            elims: dict[tuple[int, int], list[int]] = {}
            if pat["orientation"] == "row":
                r = pat["floor"][0][0]
                cols = {c for _, c in pat["floor"]}
                for c in range(9):
                    if c not in cols and m[r, c, digit]:
                        elims.setdefault((r, c), []).append(int(digit + 1))
            else:
                c = pat["floor"][0][1]
                rows = {r for r, _ in pat["floor"]}
                for r in range(9):
                    if r not in rows and m[r, c, digit]:
                        elims.setdefault((r, c), []).append(int(digit + 1))
            if elims:
                out[n].append({"type": "ur_type2", "eliminations": list(elims.items())})


def find_ur_type2b(mask: np.ndarray, out: list[list[dict]]) -> None:
    """UR Type 2b: block-locked extension of UR2."""
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for pat in _ur2_patterns(m):
            block = pat["block"]
            if block is None:
                continue
            digit = pat["extra"]
            floor = set(pat["floor"])
            elims: dict[tuple[int, int], list[int]] = {}
            for r, c in BLOCKS[block]:
                if (r, c) not in floor and m[r, c, digit]:
                    elims.setdefault((r, c), []).append(int(digit + 1))
            if elims:
                out[n].append({"type": "ur_type2b", "eliminations": list(elims.items())})

