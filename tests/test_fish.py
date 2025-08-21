import numpy as np

from strategies.fish import find_x_wing_rows, find_swordfish_rows


def test_x_wing_and_swordfish():
    # X-Wing on digit1 rows
    mask = np.zeros((1, 9, 9), dtype=np.uint16)
    bit1 = 1 << 0
    rows = [0, 2]
    cols = [0, 2]
    for r in rows:
        for c in cols:
            mask[0, r, c] |= bit1
    for r in range(9):
        if r not in rows:
            for c in cols:
                mask[0, r, c] |= bit1
    out = [[]]
    find_x_wing_rows(mask, out)
    assert any(1 in dict(ded["eliminations"]).get((1, 0), []) for ded in out[0])
    # Swordfish on digit2 rows
    mask2 = np.zeros((1, 9, 9), dtype=np.uint16)
    bit2 = 1 << 1
    rows3 = [0, 1, 2]
    cols3 = [0, 1, 2]
    for r in rows3:
        for c in cols3:
            mask2[0, r, c] |= bit2
    for r in range(3, 9):
        for c in cols3:
            mask2[0, r, c] |= bit2
    out2 = [[]]
    find_swordfish_rows(mask2, out2)
    assert any(2 in dict(ded["eliminations"]).get((3, 0), []) for ded in out2[0])
