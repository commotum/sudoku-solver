import numpy as np

from strategies.singles import (
    find_naked_singles,
    find_hidden_singles_rows,
)

FULL = (1 << 9) - 1

def test_naked_and_hidden_singles():
    mask = np.full((1, 9, 9), FULL, dtype=np.uint16)
    # Naked single at (0,0) digit 5
    mask[0, 0, 0] = 1 << 4
    # Hidden single for digit 2 in row 0 at (0,1)
    mask[0, 0, 1] = (1 << 1) | (1 << 2)
    for c in range(9):
        if c != 1:
            mask[0, 0, c] &= np.uint16(FULL & ~(1 << 1))
    out = [[]]
    find_naked_singles(mask, out)
    assert out[0] == [{"type": "naked_single", "position": (0, 0), "value": 5}]
    out2 = [[]]
    find_hidden_singles_rows(mask, out2)
    assert out2[0] == [{"type": "hidden_single_row", "position": (0, 1), "value": 2}]
