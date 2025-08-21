import numpy as np
import pytest

from strategies.subsets import find_naked_subsets, find_hidden_subsets

FULL = (1 << 9) - 1

@pytest.mark.parametrize("k, stype", [(2, "pair"), (3, "triple"), (4, "quad")])
def test_naked_subsets(k, stype):
    mask = np.full((1, 9, 9), FULL, dtype=np.uint16)
    patterns = {
        2: [(1, 2), (1, 2)],
        3: [(1, 2), (2, 3), (1, 3)],
        4: [(1, 2), (2, 3), (3, 4), (1, 4)],
    }[k]
    for idx, digs in enumerate(patterns):
        bits = 0
        for d in digs:
            bits |= 1 << (d - 1)
        mask[0, 0, idx] = bits
    out = [[]]
    find_naked_subsets(mask, out)
    assert any(d["type"] == f"naked_{stype}" for d in out[0])

@pytest.mark.parametrize("k, stype", [(2, "pair"), (3, "triple"), (4, "quad")])
def test_hidden_subsets(k, stype):
    mask = np.full((1, 9, 9), FULL, dtype=np.uint16)
    digits = list(range(1, k + 1))
    for c in range(9):
        if c >= k:
            for d in digits:
                mask[0, 0, c] &= np.uint16(FULL & ~(1 << (d - 1)))
    out = [[]]
    find_hidden_subsets(mask, out)
    assert any(d["type"] == f"hidden_{stype}" for d in out[0])
