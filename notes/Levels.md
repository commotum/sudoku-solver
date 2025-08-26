# Nine by Nine

Nine-by-Nine is a NumPy-accelerated Sudoku engine built to generate explainable, human-like reasoning traces and full step-by-step resolution paths for spatiotemporal reasoning datasets. 




The solution grid G ∈ uint8^{9×9} holds the 

To track each intermediate step in the resolution process, the Nine-by-Nine engine uses two arrays to jointly capture a complete and consistent portrait of the puzzle at that timestep. 

To track each intermediate step in the resolution process, the Nine-by-Nine engine maintains two companion arrays that jointly describe the 

joint arrays It's solver maintains two companion arrays that jointly describe the  

The engine maintains two companion arrays that jointly describe the puzzle at each step. The solution grid G ∈ uint8^{9×9} holds committed numbers (0 = empty, 1..9 = placed). The candidate tensor C ∈ bool^{9×9×9} is a possibilities cube: C[r,c,n] is True exactly when number n+1 remains admissible at cell (r,c), so the slice C[r,c,:] lists all remaining options for that cell. Rules read simple slices of C across rc/rn/cn/bn to detect Singles (counting Trues), and when a number is fixed we set G[r,c]=n+1 and perform slice-based eliminations in C (row/column/block) so the two arrays stay mutually consistent as the solve progresses.

The engine maintains two synchronized views of the same puzzle state

The engine maintains two arrays: a **solution grid** `G ∈ uint8^{9×9}` where `0` denotes empty and `1..9` are placed numbers, and a **candidate tensor** `C ∈ bool^{9×9×9}`. Entry `C[r,c,n]` encodes the predicate **“number `n+1` is currently admissible at cell `(r,c)` under Sudoku rules”** (with `r,c,n ∈ {0..8}`); equivalently, the 9-long slice `C[r,c,:]` enumerates **all remaining candidates** for that cell.


Design:
It uses a 


# Level 0: The Five Elementary Rules

## The Four Elementary Constraint Propagation Rules

If a value is asserted for a cell:

1. **ECP Cell**: Eliminate all other candidates from that cell.
2. **ECP Row**: Eliminate the asserted value as a candidate from each of the row's remaining cells.
3. **ECP Column**: Eliminate the asserted value as a candidate from each of the column's remaining cells.
4. **ECP Block**: Eliminate the asserted value as a candidate from each of the block's remaining cells.

## The Naked Single

∀r∀c {∃!n candidate(n, r, c) => value(n, r, c)}

If a cell has only one remaining candidate:

5. **NS**: Assert it as the cell's value.


# Level 1: Hidden Singles & House Interactions

– NS:∀r∀c {∃!n candidate(n, r, c) => value(n, r, c)}
– HS(row):∀r∀n {∃!c candidate(n, r, c) => value(n, r, c)}
For all rows r, and all numbers n, if there is exactly one column c in exists a single candidate for any cell 

“For every row r and every digit n: if there is exactly one column c in that row where n is allowed, put n in that one cell (r, c).”

– HS(col):∀c∀n {∃!r candidate(n, r, c) => value(n, r, c)}
– HS(blk):∀b∀n {∃!s candidate[n, b, s] => value[n, b, s]}

– HS(row): if, in abstract row-number space, there is a rn-cell (r, n) with only
one candidate (column), then assert it as the value of this rn-cell;
– HS(col): if, in abstract column-number space, there is a cn-cell (c, n) with only
one candidate (row), then assert it as the value of this cn-cell;
– HS(blk): if, in abstract block-number space, there is a bn-cell (b, n) with only
one candidate (square), then assert it as the value of this bn-cell.

import numpy as np

# C: (9, 9, 9) bool, C[r,c,n] True iff (r,c) allows digit n+1

# --- NS (Naked Single) in rc-space ---
ns_mask = (C.sum(axis=2) == 1)             # shape (9,9)
# To extract (r,c,n) triples:
r_ns, c_ns = np.where(ns_mask)
n_ns = C[r_ns, c_ns, :].argmax(axis=1)     # unique True along n-axis

# --- HS(row): “only one column for (r,n)” ---
# counts over columns for each (r,n)
rn_counts = C.sum(axis=1)                  # shape (9 rows, 9 numbers)
hsr_mask = (rn_counts == 1)
r_hsr, n_hsr = np.where(hsr_mask)
# the winning column for each (r,n)
c_hsr = C[r_hsr, :, n_hsr].argmax(axis=1)

# --- HS(col): “only one row for (c,n)” ---
# counts over rows for each (c,n)
cn_counts = C.sum(axis=0)                  # shape (9 cols, 9 numbers)
hsc_mask = (cn_counts == 1)
c_hsc, n_hsc = np.where(hsc_mask)
# the winning row for each (c,n)
r_hsc = C[:, c_hsc, n_hsc].argmax(axis=0)

# --- HS(block): “only one square for (b,n)” ---
# group rows/cols 3×3, then sum within each block
B = C.reshape(3,3, 3,3, 9)                 # (block_row, block_col, r_in_blk, c_in_blk, n) — view
bn_counts = B.sum(axis=(2,3))              # shape (3,3,9)
bn_counts = bn_counts.reshape(9,9)         # (block b=0..8, number n)
hsb_mask = (bn_counts == 1)
b_hsb, n_hsb = np.where(hsb_mask)

# recover the unique (r,c) inside each block for HS(block)
br, bc = np.divmod(b_hsb, 3)
# sub-block is a 3×3 view; find its True position
rb, cb = np.array([
    np.argwhere(B[BR, BC, :, :, n]).ravel()   # exactly one (rb,cb)
    for BR, BC, n in zip(br, bc, n_hsb)
]).T
r_hsb = br*3 + rb
c_hsb = bc*3 + cb

def assert_value(C, r, c, n):        # n = 0..8 for digit 1..9
    C[r, c, :] = False               # cell: other digits out
    C[r, :, n] = False               # row: remove n elsewhere
    C[:, c, n] = False               # column: remove n elsewhere
    br, bc = r//3, c//3
    C[br*3:(br+1)*3, bc*3:(bc+1)*3, n] = False   # block: remove n elsewhere
    C[r, c, n] = True                # keep the asserted one
