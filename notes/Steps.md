Set Notation Notes

Awesome prompt. Here’s a compact “Sudoku-as-CSP” in set notation that captures the essentials SudoRules is building, plus the core deductions it fires.

# Core sets & notation

Let

* $N=\{1,\dots,9\}$ (digits), $R=C=\{1,\dots,9\}$ (rows, cols),
* $X=R\times C$ (cells), and $B$ be the set of 9 blocks (each $b\subseteq X$).
* For a cell $x=(r,c)$, define its houses
  $\mathrm{row}(x)=\{(r,c')\}$, $\mathrm{col}(x)=\{(r',c)\}$, $\mathrm{blk}(x)\in B$.
  A *house* $H$ is any row, column, or block.
  Peers: $\mathrm{Peers}(x)=\big(\mathrm{row}(x)\cup \mathrm{col}(x)\cup \mathrm{blk}(x)\big)\setminus\{x\}$.

Candidates:

* A state is a map $C:X\to \mathcal{P}(N)$.
  For $x\in X$, $C(x)\subseteq N$ is the current candidate set of $x$.
* For a house $H$ and digit $n$, positions of $n$ in $H$ are
  $\mathrm{Pos}(H,n)=\{x\in H\mid n\in C(x)\}$.

Assignment semantics (value placed): $x\gets n$ means $C(x)=\{n\}$ and for all $y\in \mathrm{Peers}(x)$, remove $n$ from $C(y)$.

---

# Fundamental rules (few but powerful)

### 1) Cell single (a.k.a. naked single)

If $|C(x)|=1$, let $C(x)=\{n\}$. Then assign $x\gets n$.

### 2) House single (a.k.a. hidden single)

If $|\mathrm{Pos}(H,n)|=1$ with $\mathrm{Pos}(H,n)=\{x\}$, then assign $x\gets n$.

### 3) General *cover* rule (unifies pointing & claiming)

For any two houses $H_1,H_2$ that overlap (e.g., a row and the block it intersects) and any $n\in N$:

* If $\mathrm{Pos}(H_1,n)\subseteq H_1\cap H_2$, then
  eliminate $n$ from $H_2\setminus H_1$:
  $\forall y\in (H_2\setminus H_1):\; C(y)\leftarrow C(y)\setminus\{n\}$.
  (This is “pointing”.)
* Symmetrically, if $\mathrm{Pos}(H_2,n)\subseteq H_1\cap H_2$, eliminate $n$ from $H_1\setminus H_2$.
  (This is “claiming”.)

### 4) Naked subset (pairs/triples/quads)

Let $H$ be a house and $K\subseteq H$ with $|K|=k$. Define
$U=\bigcup_{x\in K} C(x)$.
If $|U|=k$ (i.e., exactly $k$ digits occupy exactly these $k$ cells), then

$$
\forall y\in H\setminus K:\; C(y)\leftarrow C(y)\setminus U .
$$

### 5) Hidden subset (pairs/triples/quads)

Let $H$ be a house and $D\subseteq N$ with $|D|=k$. Define
$K=\bigcup_{n\in D}\mathrm{Pos}(H,n)$.
If $|K|=k$ (i.e., these $k$ digits occur only in these $k$ cells), then

$$
\forall x\in K:\; C(x)\leftarrow C(x)\cap D .
$$

### 6) $k$-Fish (X-Wing/Swordfish/Jellyfish) — row form

Fix $n\in N$. Choose $R^\*\subseteq R$ with $|R^\*|=k$. Let

$$
C^\* \;=\; \bigcup_{r\in R^\*}\{\, c\in C \mid (r,c)\in \mathrm{Pos}(\mathrm{row}(r),n)\,\}.
$$

If $|C^\*|=k$ and for all $r\in R^\*$,
$\{\,c\mid (r,c)\in \mathrm{Pos}(\mathrm{row}(r),n)\,\}\subseteq C^\*$,
then eliminate $n$ from all cells in rows $R\setminus R^\*$ at columns $C^\*$:

$$
\forall r\notin R^\*,\;\forall c\in C^\*:\; C(r,c)\leftarrow C(r,c)\setminus\{n\}.
$$

(Transpose rows/cols for the column form.)

### 7) Uniqueness (UR Type 1) — a minimal statement

Let $r_1\neq r_2$, $c_1\neq c_2$, and $Q=\{(r_i,c_j): i,j\in\{1,2\}\}$.
If there exists $D\subseteq N$ with $|D|=2$ such that

* for three $x\in Q$, $C(x)=D$,
* for the fourth $x_0\in Q$, $D\subseteq C(x_0)$ and $\exists d\in C(x_0)\setminus D$,
  then to preserve uniqueness $x_0$ must take $d$: $C(x_0)=\{d\}$.

---

# (Optional) Multi-space view (rn/cn/bn)

The same candidate facts can be projected into *rn*, *cn*, *bn* spaces:

$$
\begin{aligned}
\mathrm{Pos}_{rn}(r,n)&=\{\, c\in C\mid (r,c)\in \mathrm{Pos}(\mathrm{row}(r),n)\,\},\\
\mathrm{Pos}_{cn}(c,n)&=\{\, r\in R\mid (r,c)\in \mathrm{Pos}(\mathrm{col}(c),n)\,\},\\
\mathrm{Pos}_{bn}(b,n)&=\{\, s\in \{1,\dots,9\}\mid \text{square }s\text{ of }b\text{ contains an }n\text{-candidate}\,\}.
\end{aligned}
$$

Assignments are equivalent across these views via the natural bijections between $(r,c)$, $(r,n)$, $(c,n)$, and $(b,s)$.

---

These seven rules (two singles, one cover, two subset rules, fish, and a basic uniqueness axiom) cover the lion’s share of what the loader + modules enable, and they’re enough to express most practical deductions SudoRules performs—while staying crisp in set notation.

---

Short answer: yes. If you model candidates as arrays, the rules you listed drop out cleanly.

* **Bool tensor**: `cand[r, c, n] ∈ {0,1}` says “digit `n+1` is still possible at `(r,c)`”.
* **Bitmask grid** (my favorite): `mask[r, c] ∈ uint16` where bit `n` is set iff digit `n+1` is a candidate.

Bitmasks make subset/fish/UR detection painless (bitwise ops + popcount). Below is a compact skeleton showing the core machinery and 4 rules (naked/hidden single, pointing, claiming). The others follow the same pattern with small combinatorics.

```python
import numpy as np
from itertools import combinations

DIGS = np.arange(9)              # 0..8 represent digits 1..9
ALL = (1 << 9) - 1               # 0b1_1111_1111

# --- helpers to build house index lists ---
ROWS = [[(r, c) for c in range(9)] for r in range(9)]
COLS = [[(r, c) for r in range(9)] for c in range(9)]
BLOCKS = []
for br in range(3):
    for bc in range(3):
        BLOCKS.append([(r, c)
                       for r in range(3*br, 3*br+3)
                       for c in range(3*bc, 3*bc+3)])
HOUSES = ROWS + COLS + BLOCKS

def popcount16(x: np.ndarray) -> np.ndarray:
    # numpy's vectorized bit_count is available for integer dtype
    return x.astype(np.uint16).bit_count()

def singleton_digit(mask_rc):
    """Return digit index if mask has exactly one bit, else -1."""
    if mask_rc and (mask_rc & (mask_rc-1)) == 0:
        return int(np.log2(mask_rc))
    return -1

# --- representation ---
# grid: 9x9 np.int8 with 0 for empty, 1..9 for fixed/solved values
# mask: 9x9 np.uint16 bitmasks for candidates

def init_masks_from_grid(grid):
    mask = np.full((9,9), ALL, dtype=np.uint16)
    for r in range(9):
        for c in range(9):
            v = grid[r, c]
            if v:
                m = 1 << (v-1)
                mask[r, c] = m
                # eliminate from peers
                for rr, cc in set(ROWS[r] + COLS[c] + BLOCKS[(r//3)*3 + (c//3)]):
                    if (rr, cc) != (r, c):
                        mask[rr, cc] &= ~m
    return mask

def assign(grid, mask, r, c, d):  # d is 0..8
    vmask = 1 << d
    grid[r, c] = d+1
    mask[r, c] = vmask
    changed = False
    # remove from peers
    peers = set(ROWS[r] + COLS[c] + BLOCKS[(r//3)*3 + (c//3)])
    peers.discard((r,c))
    for rr, cc in peers:
        if mask[rr, cc] & vmask:
            mask[rr, cc] &= ~vmask
            changed = True
    return changed or True

# ----------------- RULES -----------------

def rule_naked_single(grid, mask):
    """Cell single: |C(x)|=1."""
    prog = False
    pcs = popcount16(mask)
    rs, cs = np.where((grid == 0) & (pcs == 1))
    for r, c in zip(rs, cs):
        d = singleton_digit(mask[r, c])
        prog |= assign(grid, mask, r, c, d)
    return prog

def rule_hidden_single(grid, mask):
    """House single: |Pos(H,n)|=1."""
    prog = False
    for H in HOUSES:
        # For each digit, collect presence mask over cells in H
        cells = np.array(H)
        r_idx, c_idx = cells[:,0], cells[:,1]
        for d in DIGS:
            bit = 1 << d
            present = (mask[r_idx, c_idx] & bit) != 0
            if present.sum() == 1:
                k = int(np.flatnonzero(present)[0])
                r, c = r_idx[k], c_idx[k]
                if grid[r, c] == 0:
                    prog |= assign(grid, mask, r, c, d)
    return prog

def rule_pointing_and_claiming(grid, mask):
    """
    General cover rule on row/block and col/block overlaps.
    - Pointing: in a block, digit n only appears in one row (or one col) -> remove n in that row (col) outside the block.
    - Claiming: in a row, n only appears in the cells that lie in one block -> remove n from that block outside the row.
    """
    prog = False
    # Pointing (block -> row/col)
    for bidx, B in enumerate(BLOCKS):
        cells = np.array(B); br = (bidx//3)*3; bc = (bidx%3)*3
        for d in DIGS:
            bit = 1 << d
            inB = (mask[cells[:,0], cells[:,1]] & bit) != 0
            if not inB.any(): 
                continue
            rows_in_B = {r for r in range(br, br+3)
                         if ((mask[r, bc:bc+3] & bit) != 0).any()}
            if len(rows_in_B) == 1:
                r = rows_in_B.pop()
                # eliminate in row r outside the block
                out_cols = [c for c in range(9) if not (bc <= c < bc+3)]
                row_mask = mask[r, out_cols]
                hit = (row_mask & bit) != 0
                if hit.any():
                    mask[r, out_cols] &= (~bit)
                    prog = True
            cols_in_B = {c for c in range(bc, bc+3)
                         if ((mask[br:br+3, c] & bit) != 0).any()}
            if len(cols_in_B) == 1:
                c = cols_in_B.pop()
                out_rows = [r for r in range(9) if not (br <= r < br+3)]
                col_mask = mask[out_rows, c]
                hit = (col_mask & bit) != 0
                if hit.any():
                    mask[out_rows, c] &= (~bit)
                    prog = True

    # Claiming (row/col -> block)
    for r in range(9):
        cells = np.array(ROWS[r])
        for d in DIGS:
            bit = 1 << d
            pos = (mask[cells[:,0], cells[:,1]] & bit) != 0
            if not pos.any(): 
                continue
            blocks = {(r//3)*3 + (c//3) for _, c in cells[pos]}
            if len(blocks) == 1:
                bidx = next(iter(blocks)); br = (bidx//3)*3; bc = (bidx%3)*3
                # eliminate bit in block outside row r
                rows = [rr for rr in range(br, br+3) if rr != r]
                blk = mask[rows, bc:bc+3]
                hit = (blk & bit) != 0
                if hit.any():
                    mask[rows, bc:bc+3] &= (~bit)
                    prog = True
    for c in range(9):
        cells = np.array(COLS[c])
        for d in DIGS:
            bit = 1 << d
            pos = (mask[cells[:,0], cells[:,1]] & bit) != 0
            if not pos.any(): 
                continue
            blocks = {(r//3)*3 + (c//3) for r, _ in cells[pos]}
            if len(blocks) == 1:
                bidx = next(iter(blocks)); br = (bidx//3)*3; bc = (bidx%3)*3
                cols = [cc for cc in range(bc, bc+3) if cc != c]
                blk = mask[br:br+3, cols]
                hit = (blk & bit) != 0
                if hit.any():
                    mask[br:br+3, cols] &= (~bit)
                    prog = True
    return prog
```

### Subsets, fish, UR — how they look

* **Naked subset (k≤4)** in a house `H`:
  get the 9 masks `m_i` of the cells in `H`. For each combination of `k` cells, `U = OR(m_i)`; if `popcount(U)==k`, clear bits `U` from all other cells in `H`. This is \~27·(C(9,2)+C(9,3)+C(9,4)) checks — tiny.

* **Hidden subset (k≤4)** is the dual: for each digit subset `D` (combine bits), union the *positions* where those bits appear; if exactly `k` cells, intersect those cells’ masks with `D`.

* **k-Fish** for a digit `d`:
  form a 9×9 boolean matrix `A[r,c] = (mask[r,c] & bit(d))!=0`.
  For rows: choose `k` rows; let `C*` be the union of columns with a 1 in those rows. If `|C*|==k`, clear `d` from all other rows at columns `C*`. Columns version is transposed. Limiting to `k∈{2,3,4}` is plenty.

* **UR Type 1**: enumerate each 2×2 cell rectangle `Q`. Let `U = OR(masks on Q)`. If `popcount(U)==2` and exactly three cells in `Q` equal `U`, then the fourth must keep only the extra bit (i.e., assign it).

### Solve loop

```python
def solve(grid):
    mask = init_masks_from_grid(grid.copy())
    progress = True
    while progress:
        progress = False
        progress |= rule_naked_single(grid, mask)
        progress |= rule_hidden_single(grid, mask)
        progress |= rule_pointing_and_claiming(grid, mask)
        # progress |= rule_naked_subset(grid, mask, k_max=4)
        # progress |= rule_hidden_subset(grid, mask, k_max=4)
        # progress |= rule_fish(grid, mask, k_max=4)
        # progress |= rule_ur_type1(grid, mask)
    return grid, mask
```

### How “straightforward” is it?

* **Singles & cover (pointing/claiming)**: fully vectorizable/broadcast-friendly → very straightforward.
* **Subsets/fish/UR**: clean in code, but rely on small **combinational searches** (choose k rows/digits/cells). With bitmasks, those loops are tiny and fast for Sudoku sizes.
* **Chains/whips/etc.**: those are graph search; not asked here.

If you want, I can drop a complete, runnable `numpy` solver (with subsets/fish/UR included) into a file you can tweak and benchmark.











# Overview

1. General
    - Background:
        - It defines numbers, rows, columns, blocks, and squares, essentially setting up the framework for reasoning about Sudoku grids.
        - Defines the entities used in Sudoku:
            Numbers → the symbols placed in cells (typically 1–9).
            Rows, Columns, Blocks → the basic structural units of the Sudoku grid.
            Squares → individual cells in the grid.
        - Provides a mapping system so external symbols (like digits) are mapped to internal integers.
2. 



Strategy ordering and the salience system
CSP‑Rules applies its techniques strictly in a “simplest‑first” order, achieved through a hierarchy of salience levels.
Salience is just an integer priority; the engine decrements it as it moves to more complex techniques, ensuring that easy rules fire before harder ones.

Level 0 – Basic Resolution Technique (BRT)

Contradiction detection

Elementary constraints propagation

Singles (assign a value when a CSP variable has only one candidate)

Higher levels – chain families ordered by increasing complexity
For each chain length L (the solver implements lengths up to at least 36), the salience file defines the following sequence. The excerpt below shows level 11 as a representative example; the ordering is identical at other lengths:

Typed bivalue-chains

Bivalue-chains

Typed z-chains

z-chains

Oddagons and anti‑oddagons

Typed t‑whips

t‑whips

Typed whips

Whips

g‑bivalue-chains

g2‑whips

Typed g‑whips

g‑whips

Braids

g‑braids

Extended families and forcing variants
After the base chains, more elaborate techniques become eligible, still respecting chain length:

OR₂–OR₈ forcing whips → OR₂–OR₈ whips

OR₂–OR₈ forcing g‑whips → OR₂–OR₈ g‑whips

Forcing whips, forcing g‑whips, forcing braids, forcing g‑braids

w*-whips, b*-braids

biwhips, bibraids

Fallback search
Only after all pattern-based rules fail does the solver resort to Trial‑and‑Error (T&E) or its bi-directional variant, each with their own salience to ensure they run after every deterministic rule family

In summary, Berthier’s salience system enforces a clear progression: contradiction checks and singles first, then progressively longer and more general chains, then OR‑based and forcing variants, culminating in exhaustive search only as a last resort.