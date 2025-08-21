import numpy as np

from strategies.intersections import (
    find_locked_candidates_pointing,
    find_locked_candidates_claiming,
)


def test_pointing_and_claiming():
    mask = np.zeros((1, 9, 9), dtype=np.uint16)
    bit1 = 1 << 0
    bit2 = 1 << 1
    # Pointing setup
    for r in range(3):
        for c in range(3):
            mask[0, r, c] = 0
    mask[0, 0, 0] |= bit1
    mask[0, 0, 1] |= bit1
    mask[0, 0, 4] |= bit1  # candidate to be eliminated
    out = [[]]
    find_locked_candidates_pointing(mask, out)
    assert any(1 in dict(ded["eliminations"]).get((0, 4), []) for ded in out[0])
    # Claiming setup
    mask2 = np.zeros((1, 9, 9), dtype=np.uint16)
    for r in range(3):
        for c in range(3):
            mask2[0, r, c] = 0
    mask2[0, 0, 0] |= bit2
    mask2[0, 0, 1] |= bit2
    mask2[0, 1, 2] |= bit2  # cell in block outside row0
    out2 = [[]]
    find_locked_candidates_claiming(mask2, out2)
    assert any(2 in dict(ded["eliminations"]).get((1, 2), []) for ded in out2[0])
