Awesome—let’s make a clean, repeatable “rule card” you can use for every rule, and then I’ll fill it out for **Hidden Single (Row)** using your exact data structures:

* a **9×9 `grid`** of ints in `{0..9}` where `0` = empty, `1..9` = placed digit
* a **9×9×9 `C`** boolean tensor where `C[r,c,n]` is `True` iff digit `(n+1)` is a candidate at `(r,c)`

---

# Rule Card — Template

**Rule Name (English):**
**Abbrev:**
**Purpose (1 line):**

**Set Notation:**
**Spoken English (symbol-faithful):**

**Scope (quantifiers → loops):**

* Variables and domains
* Data the rule reads (grid / candidates)

**Condition (IF):**

* Math statement (counts/uniqueness)
* NumPy “vectorized find” (what to compute)

**Action (THEN):**

* Math action (`value(...)`)
* NumPy apply (placement + ECP updates)

**Notes / Guards:**

* What makes an application “effective”?
* Edge cases / contradictions (CD)

---

# Rule Card — Hidden Single (Row)

**Rule Name (English):** Hidden Single (Row)
**Abbrev:** HS(R)
**Purpose:** Place a digit when, in a given row, that digit has exactly one possible column.

**Set Notation:**

$$
\forall r\,\forall n \;\{\, \exists!\, c\;\; candidate(n,r,c)\ \Rightarrow\ value(n,r,c) \,\}
$$

**Spoken English (symbol-faithful):**
For all rows $r$ and for all numbers $n$, if there exists **exactly one** column $c$ such that $candidate(n,r,c)$ is true, then assert $(r,c)=n$.

---

## Scope (quantifiers → loops)

* Variables: $r \in \{0..8\}$ (rows), $n \in \{0..8\}$ (index for digit $n+1$).
* Reads: `C[r, :, n]` (the candidate row-slice for digit $n+1$); optionally `grid[r,:]` to skip filled cells.

## Condition (IF)

**Math:** there exists **exactly one** $c$ with $candidate(n,r,c)=\text{True}$.

**NumPy “vectorized find”:**

```python
# C shape: (9,9,9); axis 1 = columns
rn_counts = C.sum(axis=1)                 # shape (9 rows, 9 numbers)
r_idx, n_idx = np.where(rn_counts == 1)   # all (r,n) pairs satisfying ∃! c
# recover the unique column for each (r,n)
c_idx = C[r_idx, :, n_idx].argmax(axis=1) # the (unique) c for each match
matches = list(zip(r_idx, c_idx, n_idx))  # [(r, c, n), ...] in row-major order
```

## Action (THEN)

**Math:** $value(n,r,c)$ — set cell $(r,c)$ to digit $n+1$ and propagate constraints.

**NumPy apply (placement + ECP):**

```python
def apply_HS_row(grid, C, r, c, n):
    # place value
    grid[r, c] = n + 1
    # ECP eliminations
    C[r, c, :] = False
    C[r, :, n] = False
    C[:, c, n] = False
    br, bc = r//3, c//3
    C[br*3:(br+1)*3, bc*3:(bc+1)*3, n] = False
    C[r, c, n] = True
```

**Driver (vectorized “find one, then restart”):**

```python
def HS_row_find_all(C):
    rn_counts = C.sum(axis=1)
    r_idx, n_idx = np.where(rn_counts == 1)
    if r_idx.size == 0:
        return []
    c_idx = C[r_idx, :, n_idx].argmax(axis=1)
    return list(zip(r_idx, c_idx, n_idx))

# in your precedence loop:
matches = HS_row_find_all(C)
if matches:
    r, c, n = matches[0]       # first match = “first rule that applies”
    apply_HS_row(grid, C, r, c, n)
    # then restart the rule list
```

## Notes / Guards

* **Effectiveness:** skip if `grid[r,c] != 0` (already placed), or if the action makes no change.
* **Consistency:** after placement, **CD** should never trigger; if some other state created a contradiction, you’ll detect it (some cell’s candidates become empty).
* **Index mapping:** store digits 1..9 at indices `n=0..8` (`digit = n+1`).

---

## (Mini) Cards you can clone next

### Naked Single (Cell) — NS

* **Set:** $\forall r\,\forall c \{\, \exists!\,n\ candidate(n,r,c) \Rightarrow value(n,r,c) \}$
* **Condition (NumPy):** `ns_mask = (C.sum(axis=2) == 1); r,c = np.where(ns_mask); n = C[r,c,:].argmax(1)`
* **Action:** place `(r,c)=n+1`, then ECP (same slice updates).

### Hidden Single (Column) — HS(C)

* **Set:** $\forall c\,\forall n \{\, \exists!\,r\ candidate(n,r,c) \Rightarrow value(n,r,c) \}$
* **Condition (NumPy):** `cn_counts = C.sum(axis=0); c,n = np.where(cn_counts==1); r = C[:,c,n].argmax(0)`

### Hidden Single (Block) — HS(B)

* **Set:** $\forall b\,\forall n \{\, \exists!\,s\ candidate_{bn}(n,b,s) \Rightarrow value_{bn}(n,b,s) \}$
* **Condition (NumPy):**

  ```python
  B = C.reshape(3,3, 3,3, 9)             # (BR,BC, rb,cb, n)
  bn_counts = B.sum(axis=(2,3))          # (3,3,9)
  BR, BC, n = np.where(bn_counts == 1)
  # find (rb,cb) inside each winning block:
  rbcb = [np.argwhere(B[br,bc,:,:,ni]).ravel() for br,bc,ni in zip(BR,BC,n)]
  rb, cb = np.array(rbcb).T
  r = BR*3 + rb;  c = BC*3 + cb
  ```
* **Action:** place `(r,c)=n+1`, then ECP.

### Row→Block Interaction — RiB (one eliminator example)

* **Set (plain):** if row $r$’s candidates for digit $n$ lie **inside one block** $b$, eliminate $n$ from $b \setminus r$.
* **Condition (NumPy idea):** for each `(r,n)`, compute the set of blocks hit by `np.where(C[r,:,n])`; condition is “hit count == 1”.
* **Action (NumPy):** zero out `C` in that block outside row `r` for digit `n`.

---

## Organization tips

* Keep **one markdown file per rule family** (Singles, Interactions, Subsets, Chains).
* For every rule, include the **Rule Card** sections above—copy/paste the template.
* Put tiny **NumPy test snippets** under each rule so you can unit-test “find” on synthetic boards.
* Add a **naming convention** note at top (index→digit mapping, what `0` means in `grid`).
* In your solver, implement each rule with two functions:

  * `find_all_matches_vectorized(C) -> list[(r,c,n)...]` (or eliminations)
  * `apply(grid, C, match)` (returns True if it changed state)

This gives you one place that documents **set notation, spoken English, and NumPy** for each rule, and it plugs directly into your vectorized “first match, then restart” driver.
