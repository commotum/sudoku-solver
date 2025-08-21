# SPDX-License-Identifier: MIT
import numpy as np
from strategies.uniqueness import find_ur_type1


def test_ur_type1_positive():
    candidates = np.ones((1, 9, 9, 9), dtype=bool)
    # set three cells to {1,2}
    for r, c in [(0, 0), (0, 1), (1, 0)]:
        candidates[0, r, c, :] = False
        candidates[0, r, c, 0] = True
        candidates[0, r, c, 1] = True
    # fourth cell has {1,2,3}
    candidates[0, 1, 1, :] = False
    candidates[0, 1, 1, 0:3] = True
    all_deductions = [[]]
    find_ur_type1(candidates, all_deductions)
    assert all_deductions[0] == [
        {"type": "ur_type1", "position": (1, 1), "value": 3}
    ]


def test_ur_type1_negative():
    candidates = np.ones((1, 9, 9, 9), dtype=bool)
    for r, c in [(0, 0), (0, 1), (1, 0)]:
        candidates[0, r, c, :] = False
        candidates[0, r, c, 0] = True
        candidates[0, r, c, 1] = True
    # fourth cell has {1,2,3,4} -> no deduction
    candidates[0, 1, 1, :] = False
    candidates[0, 1, 1, 0:4] = True
    all_deductions = [[]]
    find_ur_type1(candidates, all_deductions)
    assert all_deductions[0] == []
