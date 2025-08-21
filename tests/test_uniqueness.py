import numpy as np

from strategies.uniqueness import find_ur_type1

FULL = (1 << 9) - 1


def test_ur_type1_positive():
    mask = np.zeros((1, 9, 9), dtype=np.uint16)
    pair = (1 << 0) | (1 << 1)
    for r, c in [(0, 0), (0, 1), (1, 0)]:
        mask[0, r, c] = pair
    mask[0, 1, 1] = pair | (1 << 2)
    out = [[]]
    find_ur_type1(mask, out)
    assert out[0] == [{"type": "ur_type1", "position": (1, 1), "value": 3}]


def test_ur_type1_negative():
    mask = np.zeros((1, 9, 9), dtype=np.uint16)
    pair = (1 << 0) | (1 << 1)
    for r, c in [(0, 0), (0, 1), (1, 0)]:
        mask[0, r, c] = pair
    mask[0, 1, 1] = pair | (1 << 2) | (1 << 3)
    out = [[]]
    find_ur_type1(mask, out)
    assert out[0] == []
