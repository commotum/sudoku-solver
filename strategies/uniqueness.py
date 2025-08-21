"""Uniqueness strategies implemented with boolean candidate grids."""

import numpy as np


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

