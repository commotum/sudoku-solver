"""Intersection removal strategies using boolean candidate grids."""

import numpy as np

from engine.utils import ROWS, COLS, BLOCKS


def _cover(m: np.ndarray, H1, H2, digit: int):
    """Return elimination list when digit in ``H1`` is confined to ``H2``."""
    d = digit - 1
    pos = [rc for rc in H1 if m[rc][d]]
    if not pos:
        return []
    if all(rc in H2 for rc in pos):
        elims: dict[tuple[int, int], list[int]] = {}
        for r, c in H2:
            if (r, c) not in H1 and m[r, c, d]:
                elims.setdefault((r, c), []).append(digit)
        return list(elims.items())
    return []


def find_locked_candidates_pointing(mask: np.ndarray, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for B in BLOCKS:
            rows = {r for r, _ in B}
            cols = {c for _, c in B}
            for digit in range(1, 10):
                for r in rows:
                    elims = _cover(m, B, ROWS[r], digit)
                    if elims:
                        out[n].append({"type": "locked_pointing", "eliminations": elims})
                for c in cols:
                    elims = _cover(m, B, COLS[c], digit)
                    if elims:
                        out[n].append({"type": "locked_pointing", "eliminations": elims})


def find_locked_candidates_claiming(mask: np.ndarray, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for r in range(9):
            blocks = {(r // 3) * 3 + (c // 3) for _, c in ROWS[r]}
            for bidx in blocks:
                B = BLOCKS[bidx]
                for digit in range(1, 10):
                    elims = _cover(m, ROWS[r], B, digit)
                    if elims:
                        out[n].append({"type": "locked_claiming", "eliminations": elims})
        for c in range(9):
            blocks = {(r // 3) * 3 + (c // 3) for r, _ in COLS[c]}
            for bidx in blocks:
                B = BLOCKS[bidx]
                for digit in range(1, 10):
                    elims = _cover(m, COLS[c], B, digit)
                    if elims:
                        out[n].append({"type": "locked_claiming", "eliminations": elims})

