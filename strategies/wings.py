import numpy as np
from itertools import combinations

# Pre-compute peers for speed
PEERS = {}
for r in range(9):
    for c in range(9):
        peers = {(r, j) for j in range(9) if j != c}
        peers |= {(i, c) for i in range(9) if i != r}
        br, bc = (r // 3) * 3, (c // 3) * 3
        peers |= {(br + i, bc + j) for i in range(3) for j in range(3)}
        peers.remove((r, c))
        PEERS[(r, c)] = peers


def xy_wing(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    deductions: list[dict] = []
    cells = [(r, c, lattice[r, c]) for r in range(9) for c in range(9) if lattice[r, c].sum() == 2]
    for r, c, cand in cells:
        a, b = np.where(cand)[0]
        pivot = (r, c)
        # Wings sharing a with pivot
        for wr, wc, wcand in cells:
            if (wr, wc) == pivot or (wr, wc) not in PEERS[pivot]:
                continue
            if wcand[a] and wcand.sum() == 2:
                other = np.where(wcand)[0]
                other = other[other != a][0]
                # second wing sharing b and same other
                for wr2, wc2, wcand2 in cells:
                    if (wr2, wc2) == pivot or (wr2, wc2) == (wr, wc):
                        continue
                    if (wr2, wc2) not in PEERS[pivot] or (wr2, wc2) in PEERS[(wr, wc)]:
                        continue
                    if wcand2[b] and wcand2.sum() == 2:
                        other2 = np.where(wcand2)[0]
                        other2 = other2[other2 != b][0]
                        if other2 != other:
                            continue
                        # eliminate 'other' from intersection of peers of wings
                        elim_cells = PEERS[(wr, wc)] & PEERS[(wr2, wc2)]
                        elims = []
                        for er, ec in elim_cells:
                            if lattice[er, ec, other]:
                                elims.append(((er, ec), [int(other + 1)]))
                        if elims:
                            deductions.append({'type': 'xy_wing',
                                               'pivot': pivot,
                                               'wings': [(wr, wc), (wr2, wc2)],
                                               'value': int(other + 1),
                                               'eliminations': elims})
    return deductions


def xyz_wing(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    """Simplified XYZ-wing implementation."""
    deductions: list[dict] = []
    cells = [(r, c, lattice[r, c]) for r in range(9) for c in range(9) if lattice[r, c].sum() == 3]
    for r, c, cand in cells:
        pivot_vals = np.where(cand)[0]
        pivot = (r, c)
        wings = [(wr, wc, lattice[wr, wc]) for wr, wc in PEERS[pivot] if lattice[wr, wc].sum() == 2]
        for (wr1, wc1, wing1), (wr2, wc2, wing2) in combinations(wings, 2):
            vals1 = set(np.where(wing1)[0])
            vals2 = set(np.where(wing2)[0])
            common = vals1 & vals2 & set(pivot_vals)
            if len(common) != 1:
                continue
            common_val = common.pop()
            if not (vals1 <= set(pivot_vals) and vals2 <= set(pivot_vals)):
                continue
            elim_cells = PEERS[(wr1, wc1)] & PEERS[(wr2, wc2)] & PEERS[pivot]
            elims = []
            for er, ec in elim_cells:
                if lattice[er, ec, common_val]:
                    elims.append(((er, ec), [int(common_val + 1)]))
            if elims:
                deductions.append({'type': 'xyz_wing',
                                   'pivot': pivot,
                                   'wings': [(wr1, wc1), (wr2, wc2)],
                                   'value': int(common_val + 1),
                                   'eliminations': elims})
    return deductions
