1. Parse input
2. For given in givens:
    - assert value
    - elementary constraint propagation
    - 

engine



# Nine by Nine

Nine-by-Nine is a NumPy-accelerated Sudoku engine built to generate explainable, human-like reasoning traces and full step-by-step resolution paths for spatiotemporal reasoning datasets. 

The Nine-by-Nine engine models each Sudoku puzzle as a Constraint Satisfaction Problem with and uses two arrays to jointly capture a complete and consistent portrait of the puzzle for every intermediate step in the resolution process.

The first is a **solution grid** `G ∈ uint8^{9×9}` where `0` denotes an empty square and `1..9` are placed numbers, and the second is a **candidate tensor** `C ∈ bool^{9×9×9}`




Given a 9x9 grid, partially filled with numbers from 1 to 9 (the "entries" of the
problem, also called the "clues" or the "givens"), complete it with numbers from 1 to
9 so that in every of the nine rows, in every of the nine columns and in every of the
nine disjoint blocks of 3x3 contiguous cells, the following property holds:
– there is at most one occurrence of each of these numbers.

Since rows, columns and blocks play similar roles in the defining constraints,
they will naturally appear to do so in many other places and it is convenient to intro-
duce a word that makes no difference between them: a unit is either a row or a
column or a block. And we say that two cells share a unit if they are either in the
same row or in the same column or in the same block (where "or" is non exclusive).
We also say that these two cells are linked, or that they see each other. It should be
noticed that this (symmetric) relation between two cells, whichever of the three
equivalent names it is given, does not depend in any way on the content of these
cells but only on their place in the grid; it is therefore a straightforward and quasi
physical notion.

The problem statement lists the constraints a solution grid must satisfy, i.e. it
says what we want. It does not say anything about how we can obtain it: this is the
job of the resolution methods and the resolution rules on which they are based.

at any stage of the resolution process, candidates
for a cell are the numbers that are not yet explicitly known to be impossible values
for this cell.

the resolution process is a sequence of steps consisting of repeatedly
applying "resolution rules" (some of which have become very classical and some of
which may be very complex) of the general condition-action type: if some pattern
(i.e. configuration) of cells, links, values and candidates for these cells is present on
the grid, then carry out the action specified by the rule.

According to the type of their action part, such rules can be classified into three
categories:
– either assert the final value of a cell (when it is proven there is only one possi-
bility left for it); there are very few rules of this type;
– or delete some candidate(s) (which we call the target values of the pattern)
from some cell(s) (which we call the target cells of the pattern); as appears from a
quick browsing of the available literature and as will be confirmed by this book,
most resolution rules are of this type; they express specific forms of constraints
propagation; their general form is: if such a pattern is present, then it is impossible
for some value(s) to be in some cell(s) and the corresponding candidates must be
deleted from them;
– or, for some very difficult grids, recursively make a hypothesis on the value of
a cell, analyse its consequences and apply the eliminations induced by the
contradictions thus discovered;

The four simpler constraints propagation rules (obviously valid) are the direct
translation of the initial problem formulation into operational rules for managing
candidates. We call them "the (four) elementary constraints propagation rules"
(ECP):
– ECP(cell): "if a value is asserted for a cell (as is the case for the initial values),
then remove all the other candidates for this cell";
– ECP(row): "if a value is asserted for a cell (as is the case for the initial values),
then remove this value from the candidates for any other cell in the same row";
– ECP(col): "if a value is asserted for a cell (as is the case for the initial values),
then remove this value from the candidates for any other cell in the same column";
– ECP(blk): "if a value is asserted for a cell (as is the case for the initial values),
then remove this value from the candidates for any other cell in the same block".
The simpler assertion rule (also obviously valid) is called Naked-Single:
– NS: "if a cell has only one candidate left, then assert it as the only possible
value of the cell".
Together with NS, the four elementary constraints propagation rules constitute
"the (five) elementary rules".

ok, we build a hierarchy of rules progressi-
vely, based on:
– a distinction between three general classes of rules: subset rules, interaction
rules and chain rules;
– a generalised notion of logical symmetry and associated representations;
– a second guiding principle: a rule obtained from another by some (generalised
or not) logical symmetry must be granted the same logical complexity.

Moreover, to every resolution method one can associate a simple systematic
procedure for solving a puzzle:
List the all the resolution rules in a way compatible with their precedence ordering
(i.e. among the different possibilities of doing so choose one)
Loop until a solution is found (or until it is proven there can be no solution)
⎢
Do until a rule applies effectively
⎢
⎢
Take the first rule not yet tried in the list
⎢
⎢
Do until its conditions pattern effectively maps to the grid
⎢
⎢
⎢
Try all possible mappings of the conditions pattern

Introduction
25
⎢
⎢
End do
⎢
End do
⎢
Apply rule on selected matching pattern
End loop






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
