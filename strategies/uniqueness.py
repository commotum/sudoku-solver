"""Uniqueness strategies implemented with boolean candidate grids."""

import numpy as np

from engine.utils import BLOCKS


def find_bug(mask: np.ndarray, out: list[list[dict]]) -> None:
    """BUG+1 strategy (Bi-value Universal Grave).

    Detects the BUG+1 pattern where all unsolved cells are bivalue except a
    single cell with three candidates, and house-digit parity holds. The lone
    cell is solved by the digit that has no partner in any of its three houses.
    """
    N = mask.shape[0]
    pcs = mask.sum(axis=3)
    for n in range(N):
        pc = pcs[n]
        m = mask[n]
        cells3 = np.argwhere(pc == 3)
        if cells3.shape[0] != 1:
            continue
        # all other unsolved cells must be bivalue
        if np.any((pc > 1) & (pc != 2) & (pc != 3)):
            continue

        # parity checks for each house and digit
        parity_ok = True
        for d in range(9):
            for r in range(9):
                row = m[r, :, d]
                placed = np.any((pc[r] == 1) & row)
                if not placed and row.sum() != 2:
                    parity_ok = False
                    break
            if not parity_ok:
                break
            for c in range(9):
                col = m[:, c, d]
                placed = np.any((pc[:, c] == 1) & col)
                if not placed and col.sum() != 2:
                    parity_ok = False
                    break
            if not parity_ok:
                break
            for cells in BLOCKS:
                arr = np.array([m[r, c, d] for r, c in cells])
                placed = np.any([pc[r, c] == 1 and m[r, c, d] for r, c in cells])
                if not placed and arr.sum() != 2:
                    parity_ok = False
                    break
            if not parity_ok:
                break
        if not parity_ok:
            continue

        r, c = map(int, cells3[0])
        digits = np.where(m[r, c])[0]
        good: list[int] = []
        blk = (r // 3) * 3 + (c // 3)
        for d in digits:
            if (
                m[r, :, d].sum() == 1
                and m[:, c, d].sum() == 1
                and sum(m[rr, cc, d] for rr, cc in BLOCKS[blk]) == 1
            ):
                good.append(int(d))
        if len(good) == 1:
            out[n].append({
                "type": "bug",
                "position": (r, c),
                "value": int(good[0] + 1),
            })


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


def find_ur_type3(mask: np.ndarray, out: list[list[dict]]) -> None:
    """UR Type 3: different extras on the floor plus a {c,d} bivalue in the same house."""
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
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
                            a, b = rd0
                            fd0, fd1 = np.where(floor[0])[0], np.where(floor[1])[0]
                            if {a, b}.issubset(fd0) and {a, b}.issubset(fd1):
                                extras0 = set(fd0) - {a, b}
                                extras1 = set(fd1) - {a, b}
                                for c in extras0 - extras1:
                                    for d in extras1 - extras0:
                                        if c == d:
                                            continue
                                        y_cell = None
                                        for c3 in range(9):
                                            if c3 in (c1, c2):
                                                continue
                                            s = np.where(m[r2, c3])[0]
                                            if len(s) == 2 and set(s) == {c, d}:
                                                y_cell = (r2, c3)
                                                break
                                        if y_cell is None:
                                            continue
                                        elims: dict[tuple[int, int], list[int]] = {}
                                        for c4 in range(9):
                                            if c4 in (c1, c2, y_cell[1]):
                                                continue
                                            vals: list[int] = []
                                            if m[r2, c4, c]:
                                                vals.append(int(c + 1))
                                            if m[r2, c4, d]:
                                                vals.append(int(d + 1))
                                            if vals:
                                                elims[(r2, c4)] = vals
                                        if elims:
                                            out[n].append(
                                                {
                                                    "type": "ur_type3",
                                                    "eliminations": list(elims.items()),
                                                }
                                            )

                        # Vertical floor at column c2
                        roof = [x11, x21]
                        floor = [x12, x22]
                        rd0, rd1 = np.where(roof[0])[0], np.where(roof[1])[0]
                        if rd0.size == 2 and np.array_equal(rd0, rd1):
                            a, b = rd0
                            fd0, fd1 = np.where(floor[0])[0], np.where(floor[1])[0]
                            if {a, b}.issubset(fd0) and {a, b}.issubset(fd1):
                                extras0 = set(fd0) - {a, b}
                                extras1 = set(fd1) - {a, b}
                                for c in extras0 - extras1:
                                    for d in extras1 - extras0:
                                        if c == d:
                                            continue
                                        y_cell = None
                                        for r3 in range(9):
                                            if r3 in (r1, r2):
                                                continue
                                            s = np.where(m[r3, c2])[0]
                                            if len(s) == 2 and set(s) == {c, d}:
                                                y_cell = (r3, c2)
                                                break
                                        if y_cell is None:
                                            continue
                                        elims: dict[tuple[int, int], list[int]] = {}
                                        for r4 in range(9):
                                            if r4 in (r1, r2, y_cell[0]):
                                                continue
                                            vals: list[int] = []
                                            if m[r4, c2, c]:
                                                vals.append(int(c + 1))
                                            if m[r4, c2, d]:
                                                vals.append(int(d + 1))
                                            if vals:
                                                elims[(r4, c2)] = vals
                                        if elims:
                                            out[n].append(
                                                {
                                                    "type": "ur_type3",
                                                    "eliminations": list(elims.items()),
                                                }
                                            )


def find_ur_type4(mask: np.ndarray, out: list[list[dict]]) -> None:
    """UR Type 4: block-locked UR digit across the floor pair."""
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
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
                        if c1 // 3 == c2 // 3:  # floor cells within same block
                            roof = [x11, x12]
                            floor = [x21, x22]
                            rd0, rd1 = np.where(roof[0])[0], np.where(roof[1])[0]
                            if rd0.size == 2 and np.array_equal(rd0, rd1):
                                a, b = rd0
                                fd0, fd1 = np.where(floor[0])[0], np.where(floor[1])[0]
                                if {a, b}.issubset(fd0) and {a, b}.issubset(fd1):
                                    block = (r2 // 3) * 3 + (c1 // 3)
                                    for d in (a, b):
                                        cells_d = [
                                            (rr, cc)
                                            for rr, cc in BLOCKS[block]
                                            if m[rr, cc, d]
                                        ]
                                        if set(cells_d) == {(r2, c1), (r2, c2)}:
                                            d_other = b if d == a else a
                                            elims: dict[tuple[int, int], list[int]] = {}
                                            for r, c in [(r2, c1), (r2, c2)]:
                                                if m[r, c, d_other]:
                                                    elims[(r, c)] = [int(d_other + 1)]
                                            if elims:
                                                out[n].append(
                                                    {
                                                        "type": "ur_type4",
                                                        "eliminations": list(elims.items()),
                                                    }
                                                )
                                            break

                        # Vertical floor at column c2
                        if r1 // 3 == r2 // 3:  # floor cells within same block
                            roof = [x11, x21]
                            floor = [x12, x22]
                            rd0, rd1 = np.where(roof[0])[0], np.where(roof[1])[0]
                            if rd0.size == 2 and np.array_equal(rd0, rd1):
                                a, b = rd0
                                fd0, fd1 = np.where(floor[0])[0], np.where(floor[1])[0]
                                if {a, b}.issubset(fd0) and {a, b}.issubset(fd1):
                                    block = (r1 // 3) * 3 + (c2 // 3)
                                    for d in (a, b):
                                        cells_d = [
                                            (rr, cc)
                                            for rr, cc in BLOCKS[block]
                                            if m[rr, cc, d]
                                        ]
                                        if set(cells_d) == {(r1, c2), (r2, c2)}:
                                            d_other = b if d == a else a
                                            elims: dict[tuple[int, int], list[int]] = {}
                                            for r, c in [(r1, c2), (r2, c2)]:
                                                if m[r, c, d_other]:
                                                    elims[(r, c)] = [int(d_other + 1)]
                                            if elims:
                                                out[n].append(
                                                    {
                                                        "type": "ur_type4",
                                                        "eliminations": list(elims.items()),
                                                    }
                                                )
                                            break

