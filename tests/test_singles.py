import numpy as np

from strategies.singles import (
    find_naked_singles,
    find_hidden_singles_rows,
)


def test_naked_and_hidden_singles():
    mask = np.ones((1, 9, 9, 9), dtype=bool)
    # Naked single at (0,0) digit 5
    mask[0, 0, 0, :] = False
    mask[0, 0, 0, 4] = True
    # Hidden single for digit 2 in row 0 at (0,1)
    mask[0, 0, 1, :] = False
    mask[0, 0, 1, [1, 2]] = True
    for c in range(9):
        if c != 1:
            mask[0, 0, c, 1] = False
    out = [[]]
    find_naked_singles(mask, out)
    assert out[0] == [{"type": "naked_single", "position": (0, 0), "value": 5}]
    out2 = [[]]
    find_hidden_singles_rows(mask, out2)
    assert out2[0] == [{"type": "hidden_single_row", "position": (0, 1), "value": 2}]
