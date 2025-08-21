import numpy as np

from strategies.uniqueness import find_ur_type1


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
