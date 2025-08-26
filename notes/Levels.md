# Nine by Nine

Nine by Nine is a a human‑style Sudoku solver that  that generates step‑by‑step solving sequences.

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