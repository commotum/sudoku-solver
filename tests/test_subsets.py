import numpy as np
import pytest

from strategies.subsets import find_naked_subsets, find_hidden_subsets


@pytest.mark.parametrize("k, stype", [(2, "pair"), (3, "triple"), (4, "quad")])
def test_naked_subsets(k, stype):
    mask = np.ones((1, 9, 9, 9), dtype=bool)
    patterns = {
        2: [(1, 2), (1, 2)],
        3: [(1, 2), (2, 3), (1, 3)],
        4: [(1, 2), (2, 3), (3, 4), (1, 4)],
    }[k]
    for idx, digs in enumerate(patterns):
        mask[0, 0, idx, :] = False
        for d in digs:
            mask[0, 0, idx, d - 1] = True
    out = [[]]
    find_naked_subsets(mask, out)
    assert any(d["type"] == f"naked_{stype}" for d in out[0])


@pytest.mark.parametrize("k, stype", [(2, "pair"), (3, "triple"), (4, "quad")])
def test_hidden_subsets(k, stype):
    mask = np.ones((1, 9, 9, 9), dtype=bool)
    digits = list(range(1, k + 1))
    for c in range(9):
        if c >= k:
            for d in digits:
                mask[0, 0, c, d - 1] = False
    out = [[]]
    find_hidden_subsets(mask, out)
    assert any(d["type"] == f"hidden_{stype}" for d in out[0])
