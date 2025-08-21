import numpy as np
from itertools import combinations

ALL_CANDIDATES = (1 << 9) - 1  # 0b1_1111_1111

# Precompute houses
ROWS = [[(r, c) for c in range(9)] for r in range(9)]
COLS = [[(r, c) for r in range(9)] for c in range(9)]
BLOCKS = []
for br in range(3):
    for bc in range(3):
        BLOCKS.append(
            [
                (r, c)
                for r in range(br * 3, br * 3 + 3)
                for c in range(bc * 3, bc * 3 + 3)
            ]
        )
HOUSES = ROWS + COLS + BLOCKS

# Peers for assignments
PEERS = [[set() for _ in range(9)] for _ in range(9)]
for r in range(9):
    for c in range(9):
        peers = set(ROWS[r] + COLS[c] + BLOCKS[(r // 3) * 3 + (c // 3)])
        peers.remove((r, c))
        PEERS[r][c] = peers

# Popcount lookup for 9-bit masks
POPCOUNT = np.array([bin(i).count("1") for i in range(1 << 9)], dtype=np.uint8)

def popcount16(mask: np.ndarray) -> np.ndarray:
    """Vectorized population count for uint16 mask arrays."""
    return POPCOUNT[mask]

def digits_from_mask(mask_rc: int) -> list[int]:
    """Return list of 1-based digits present in mask value."""
    return [d + 1 for d in range(9) if mask_rc & (1 << d)]

def Pos(mask: np.ndarray, H: list[tuple[int, int]], n: int) -> list[tuple[int, int]]:
    """Positions of digit n (1-based) inside house H for a single grid mask."""
    bit = 1 << (n - 1)
    return [(r, c) for r, c in H if mask[r, c] & bit]

def candidate_mask_init(grids: np.ndarray) -> np.ndarray:
    """Compute uint16 candidate masks for batch of grids."""
    if grids.ndim == 2:
        grids = grids[None, ...]
    N = grids.shape[0]
    mask = np.full((N, 9, 9), ALL_CANDIDATES, dtype=np.uint16)
    for n in range(N):
        grid = grids[n]
        for r in range(9):
            for c in range(9):
                val = int(grid[r, c])
                if val:
                    bit = 1 << (val - 1)
                    mask[n, r, c] = bit
                    for rr, cc in PEERS[r][c]:
                        mask[n, rr, cc] &= ~bit
    return mask

def assign(grid: np.ndarray, mask: np.ndarray, r: int, c: int, d0idx: int) -> None:
    """Assign digit index d0idx (0-based) to cell (r,c) updating peers."""
    bit = 1 << d0idx
    grid[r, c] = d0idx + 1
    mask[r, c] = bit
    for rr, cc in PEERS[r][c]:
        mask[rr, cc] &= ~bit

def apply_deductions(grids: np.ndarray, mask: np.ndarray, all_deductions: list[list[dict]]) -> int:
    """Apply recorded deductions to grids and masks in-place."""
    if grids.ndim == 2:
        grids = grids[None, ...]
        mask = mask[None, ...]
    changes = 0
    for n, deds in enumerate(all_deductions):
        for ded in deds:
            if "value" in ded and "position" in ded:
                r, c = ded["position"]
                d = ded["value"] - 1
                if grids[n, r, c] == 0:
                    assign(grids[n], mask[n], r, c, d)
                    changes += 1
            if "eliminations" in ded:
                for (r, c), vals in ded["eliminations"]:
                    for val in vals:
                        bit = 1 << (val - 1)
                        if mask[n, r, c] & bit:
                            mask[n, r, c] &= ~bit
                            changes += 1
    return changes
