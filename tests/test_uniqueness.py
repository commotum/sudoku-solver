import numpy as np

from strategies.uniqueness import (
    find_ur_type1,
    find_ur_type2,
    find_ur_type2b,
)


def test_ur_type1_positive():
    mask = np.zeros((1, 9, 9, 9), dtype=bool)
    for r, c in [(0, 0), (0, 1), (1, 0)]:
        mask[0, r, c, 0] = True
        mask[0, r, c, 1] = True
    mask[0, 1, 1, 0] = True
    mask[0, 1, 1, 1] = True
    mask[0, 1, 1, 2] = True
    out = [[]]
    find_ur_type1(mask, out)
    assert out[0] == [{"type": "ur_type1", "position": (1, 1), "value": 3}]


def test_ur_type1_negative():
    mask = np.zeros((1, 9, 9, 9), dtype=bool)
    for r, c in [(0, 0), (0, 1), (1, 0)]:
        mask[0, r, c, 0] = True
        mask[0, r, c, 1] = True
    mask[0, 1, 1, 0] = True
    mask[0, 1, 1, 1] = True
    mask[0, 1, 1, 2] = True
    mask[0, 1, 1, 3] = True
    out = [[]]
    find_ur_type1(mask, out)
    assert out[0] == []


def test_ur_type2_positive():
    mask = np.zeros((1, 9, 9, 9), dtype=bool)
    # Roof cells with digits 1 and 2
    for r, c in [(0, 0), (0, 1)]:
        mask[0, r, c, 0] = True
        mask[0, r, c, 1] = True
    # Floor cells with digits 1,2,3
    for r, c in [(1, 0), (1, 1)]:
        mask[0, r, c, 0] = True
        mask[0, r, c, 1] = True
        mask[0, r, c, 2] = True
    # Another cell in the floor row containing digit 3
    mask[0, 1, 2, 2] = True
    out = [[]]
    find_ur_type2(mask, out)
    assert out[0] == [
        {"type": "ur_type2", "eliminations": [((1, 2), [3])]},
    ]


def test_ur_type2b_positive():
    mask = np.zeros((1, 9, 9, 9), dtype=bool)
    # Roof cells with digits 1 and 2
    for r, c in [(0, 0), (0, 1)]:
        mask[0, r, c, 0] = True
        mask[0, r, c, 1] = True
    # Floor cells with digits 1,2,3 (same block)
    for r, c in [(1, 0), (1, 1)]:
        mask[0, r, c, 0] = True
        mask[0, r, c, 1] = True
        mask[0, r, c, 2] = True
    # Cell in the same block but outside the floor containing digit 3
    mask[0, 0, 2, 2] = True
    out = [[]]
    find_ur_type2b(mask, out)
    assert out[0] == [
        {"type": "ur_type2b", "eliminations": [((0, 2), [3])]},
    ]

