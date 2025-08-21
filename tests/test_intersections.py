import numpy as np

from strategies.intersections import (
    find_locked_candidates_pointing,
    find_locked_candidates_claiming,
)


def test_pointing_and_claiming():
    mask = np.zeros((1, 9, 9, 9), dtype=bool)
    # Pointing setup
    mask[0, 0, 0, 0] = True
    mask[0, 0, 1, 0] = True
    mask[0, 0, 4, 0] = True  # candidate to be eliminated
    out = [[]]
    find_locked_candidates_pointing(mask, out)
    assert any(1 in dict(ded["eliminations"]).get((0, 4), []) for ded in out[0])
    # Claiming setup
    mask2 = np.zeros((1, 9, 9, 9), dtype=bool)
    mask2[0, 0, 0, 1] = True
    mask2[0, 0, 1, 1] = True
    mask2[0, 1, 2, 1] = True  # cell in block outside row0
    out2 = [[]]
    find_locked_candidates_claiming(mask2, out2)
    assert any(2 in dict(ded["eliminations"]).get((1, 2), []) for ded in out2[0])
