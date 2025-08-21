# SPDX-License-Identifier: MIT
"""Uniqueness strategies: Unique Rectangle Type 1."""
from __future__ import annotations

import numpy as np


def _mask_array(candidates: np.ndarray) -> np.ndarray:
    """Return uint16 mask representation from boolean candidate grid."""
    digit_bits = (1 << np.arange(9, dtype=np.uint16))
    return np.tensordot(candidates.astype(np.uint16), digit_bits, axes=([3], [0]))


def find_ur_type1(candidates: np.ndarray, all_deductions: list[list[dict]]) -> None:
    """Detect Unique Rectangle (UR) Type 1 opportunities.

    Parameters
    ----------
    candidates : np.ndarray
        Boolean candidate masks of shape ``(N, 9, 9, 9)``.
    all_deductions : list[list[dict]]
        Accumulates deductions per puzzle.
    """
    masks = _mask_array(candidates)  # shape (N,9,9)
    N = masks.shape[0]
    for r1 in range(8):
        for r2 in range(r1 + 1, 9):
            for c1 in range(8):
                for c2 in range(c1 + 1, 9):
                    # Order of rectangle cells: (r1,c1),(r1,c2),(r2,c1),(r2,c2)
                    cell_masks = masks[:, [r1, r1, r2, r2], [c1, c2, c1, c2]]  # (N,4)
                    for t in range(4):
                        others = np.delete(cell_masks, t, axis=1)  # (N,3)
                        target = cell_masks[:, t]
                        base_equal = (others[:, 0] == others[:, 1]) & (others[:, 1] == others[:, 2])
                        base_mask = others[:, 0]
                        base_two = base_mask.bit_count() == 2
                        cond_base = base_equal & base_two
                        if not np.any(cond_base):
                            continue
                        # target must contain base and have exactly one extra digit
                        target_mask = target
                        contains = (target_mask & base_mask) == base_mask
                        extra_mask = target_mask ^ base_mask
                        single_extra = extra_mask.bit_count() == 1
                        cond = cond_base & contains & single_extra
                        idxs = np.where(cond)[0]
                        if idxs.size == 0:
                            continue
                        # Map t to actual cell coordinates
                        coords = [
                            (r1, c1),
                            (r1, c2),
                            (r2, c1),
                            (r2, c2),
                        ]
                        tr, tc = coords[t]
                        for n in idxs:
                            bit = extra_mask[n]
                            digit = (int(bit).bit_length() - 1) + 1  # convert bit to digit 1..9
                            all_deductions[n].append(
                                {
                                    "type": "ur_type1",
                                    "position": (tr, tc),
                                    "value": digit,
                                }
                            )
