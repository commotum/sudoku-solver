import numpy as np

from strategies.uniqueness import find_bug


def test_bug_negative():
    mask = np.zeros((1, 9, 9, 9), dtype=bool)
    solved = np.array([
        [1,2,3,4,5,6,7,8,9],
        [4,5,6,7,8,9,1,2,3],
        [7,8,9,1,2,3,4,5,6],
        [2,3,4,5,6,7,8,9,1],
        [5,6,7,8,9,1,2,3,4],
        [8,9,1,2,3,4,5,6,7],
        [3,4,5,6,7,8,9,1,2],
        [6,7,8,9,1,2,3,4,5],
        [9,1,2,3,4,5,6,7,8],
    ]) - 1
    for r in range(9):
        for d in range(9):
            c = np.where(solved[r] == d)[0][0]
            mask[0, r, c, d] = True
            mask[0, r, (c + 3) % 9, d] = True
    out = [[]]
    find_bug(mask, out)
    assert out[0] == []
