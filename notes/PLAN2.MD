Look at our BIG PICTURE PLAN HERE:

*WE WILL NOT IMPLEMENT ALL THE STEPS HERE TODAY - SEE END FOR DETAILS*

Status of Strategy Implementation
The solver currently supports only singles, subsets, and basic intersection techniques, as listed in the “Implemented Strategies” section of the README. Files for fish, wing, and chain techniques exist but contain only placeholder comments, meaning these methods are not yet implemented:

fish.py – intended for X-Wing and Swordfish

wings.py – intended for XY-Wing and XYZ-Wing

chains.py – intended for Coloring, Forcing Chain, and Nishio

Plan to Complete Remaining Strategies
Enable elimination handling

Extend utils.apply_deductions (and/or a candidate-management helper) so elimination-type deductions can update candidates immediately, allowing advanced strategies to propagate their effects.

Implement missing strategy families

Fish strategies (fish.py): X-Wing and Swordfish with a generic pattern-scanning helper.

Wing strategies (wings.py): XY-Wing and XYZ-Wing using bivalue/trivalue pivots to remove candidates.

Chain strategies (chains.py): Coloring, Forcing Chain, and Nishio to capture implication-based eliminations or forced fills.

Integrate and register

Add each new strategy function to STRATEGY_FUNCTIONS in strategies/strategies.py and expand the default strategy list in solver.py as they become stable.

Testing & validation

Create small puzzle sets or unit tests that exercise each strategy.

Confirm eliminations/fills are correct and improve overall solver progress without conflicts.

Following this roadmap will complete the solver’s planned strategy suite and enable more human-style deduction sequences across harder puzzles.

=========================================

Now look at the taxonomy here:

To make the code more modular and maintainable, yes, breaking it into multiple files is a good idea—especially as we add more strategies, which could make a single `human_strategies.py` file bloated and hard to navigate. Since your goal is to generate extended sequences of solving steps (mimicking human logic) for each puzzle in the dataset, organizing by strategy type or complexity will help keep related functions together and make it easier to extend (e.g., adding new strategies without touching unrelated code).

### Suggested File Names and Structure
Based on the taxonomy below, I recommend grouping strategies logically by their complexity and type of operation. This aligns with common Sudoku solver implementations, where simpler strategies (like singles) are applied first in the solver loop for efficiency, before escalating to more complex ones (like chains). Here's a breakdown:

- **singles.py**: For basic single-candidate strategies (Naked Single and Hidden Single). These are the simplest and most frequent, resulting in direct certainties (filling a cell).
- **subsets.py**: For pair/triplet/quad strategies (Naked Pair/Triplet/Quad and Hidden Pair/Triplet/Quad). These operate on small groups (2-4) of cells or candidates, often leading to eliminations.
- **intersections.py**: For Locked Candidates (also known as Pointing Pairs/Triples or Claiming). This focuses on intersections between units, leading to eliminations.
- **fish.py**: For grid-pattern strategies like X-Wing and Swordfish (extendable to Jellyfish if needed). These are column/row-based eliminations on larger patterns.
- **wings.py**: For hinge/chain starter strategies like XY-Wing and XYZ-Wing. These introduce simple chain logic for eliminations.
- **chains.py**: For advanced chain-based strategies (Coloring, Forcing Chain, Nishio). These are more complex, often involving graph-like traversals or trials, and can lead to either certainties or eliminations.

This gives us 6 files instead of 2, but they're small and focused—better for scalability. If you prefer just two files to start, we could do `basic_strategies.py` (singles + intersections + subsets) and `advanced_strategies.py` (fish + wings + chains), but the finer split will pay off as we implement more.

Each file would contain:
- The strategy functions (e.g., `find_naked_singles(candidates, all_deductions)`).
- Possibly sub-functions if needed (e.g., separate row/col/box handlers for hidden subsets).

Then, create a central `strategies.py` file that:
- Imports all the strategy functions from the above files.
- Maintains the `STRATEGY_FUNCTIONS` dictionary (mapping names to functions).
- Handles group expansions (e.g., `'hidden_single'` → row/col/box variants).
- Exports `find_deductions_batch` (which computes candidates once, then calls the requested strategies).

This way, your solver can import from `strategies.py` without knowing the internal file split.

### Outline of the Whole Repo
Here's how the repo could look and work together. The flow is: Download/process data → Load puzzles by difficulty → For each puzzle, run a solver loop that applies strategies step-by-step, recording each deduction/elimination as part of a "sequence" (e.g., a list of states or steps) → Save or analyze the sequences.

```
sudoku-solver-repo/
├── dataset_download.py     # Downloads CSVs from HF, processes into difficulty-bucketed .npy files (inputs/outputs as 9x9 arrays).
├── strategies/             # Directory for strategy modules (to keep root clean).
│   ├── __init__.py         # Empty, or exports all for easy imports.
│   ├── strategies.py       # Central hub: imports all functions, defines STRATEGY_FUNCTIONS dict, implements find_deductions_batch.
│   ├── singles.py          # Naked Single, Hidden Single (row/col/box).
│   ├── subsets.py          # Naked/Hidden Pairs/Triplets/Quads (row/col/box variants).
│   ├── intersections.py    # Locked Candidates (pointing and claiming).
│   ├── fish.py             # X-Wing, Swordfish.
│   ├── wings.py            # XY-Wing, XYZ-Wing.
│   └── chains.py           # Coloring, Forcing Chain, Nishio.
├── solver.py               # The core solver: Loads .npy files, for each puzzle: initialize grid, loop until solved/stuck: compute candidates → find deductions (via strategies.py) → apply fills/eliminations → record step (e.g., as a dict: {'step': i, 'grid_state': copy_of_grid, 'deductions': list_of_dicts}). Handles batching for efficiency. Outputs sequences as .npy or JSON per difficulty.
├── utils.py                # Helpers: Grid validation (is_valid_sudoku), pretty-print grid, apply_deduction (fill or eliminate on grid), maybe candidate computation if we extract it.
├── main.py                 # Entry point: Args for difficulty levels/subsample, calls dataset_download if needed, then solver, perhaps prints stats (e.g., avg steps per difficulty).
├── requirements.txt        # numpy, huggingface_hub, tqdm, etc.
├── data/                   # Generated: lvl-*-inputs.npy, lvl-*-outputs.npy, and later sequence files.
└── README.md               # Explains setup, how to run, and strategy taxonomy.
```

**How It Works Together**:
1. Run `dataset_download.py` (once): Fetches data, buckets by difficulty into `data/`.
2. In `main.py`: Parse args (e.g., difficulties to process), load inputs/outputs from .npy.
3. Call functions from `solver.py`: For a batch of puzzles (e.g., all level 5), initialize grids from inputs.
4. Solver loop per puzzle (or batched where possible):
   - While not solved and progress possible:
     - Call `find_deductions_batch` from `strategies.py` with desired strategies (e.g., start with basics, escalate if stuck).
     - Apply deductions: Fill certainties first, then eliminations. Update grid.
     - Record the step: Current grid snapshot + list of deductions applied.
   - Validate against output (solution) if needed.
   - Collect sequences (lists of steps) for ML dataset generation.
5. Save sequences (e.g., per difficulty as .npy: array of [puzzle_id, step_id, grid_flat, deductions_json]).

This structure supports your "extended sequence" goal: Each sequence is a chain of states from initial grid to solved, with human-like steps annotated by strategy type.

### Taxonomy of Strategies
Sudoku strategies can be classified in a few ways, but no single taxonomy is perfect—they overlap. I'll break them down by:
- **Action Type**: Does it result in a *certainty* (definite fill of a cell) or an *operation on unknowns* (eliminate candidates, reducing possibilities without filling)?
- **Complexity/Size**: Based on the number of cells/candidates involved (single=1, double/pair=2, triple=3, quad=4, or more for chains).
- **Scope**: Unit-based (row/col/box), intersection (between units), pattern/grid-wide, or chain/trial (implications across the grid).
- **Notes**: Brief description, why it's "human-like," and typical order in solvers (simpler first to avoid unnecessary complexity).

| Strategy              | Action Type          | Complexity/Size | Scope              | Notes |
|-----------------------|----------------------|-----------------|--------------------|-------|
| **Naked Single**     | Certainty (fill cell) | Single (1 candidate in cell) | Cell-only | Simplest: Cell has only 1 possible candidate left after basic eliminations. Applied first in most solvers. |
| **Hidden Single**    | Certainty (fill cell) | Single (1 cell for a candidate in unit) | Unit (row/col/box) | Candidate appears in only 1 cell in a unit; fill it. Similar to naked but "hidden" among other candidates. |
| **Locked Candidates** | Operation on unknowns (eliminate candidates) | Pair/Triple (2-3 cells in intersection) | Intersection (box-row/col) | Candidate locked to a box-line intersection; eliminate from rest of line or box. AKA Pointing (box→line) or Claiming (line→box). |
| **Naked Pair/Triplet/Quad** | Operation on unknowns (eliminate candidates) | Pair (2), Triple (3), Quad (4) cells/candidates | Unit (row/col/box) | Group of cells in unit with exactly those candidates; eliminate them from other cells in unit. |
| **Hidden Pair/Triplet/Quad** | Operation on unknowns (eliminate candidates) | Pair (2), Triple (3), Quad (4) candidates/cells | Unit (row/col/box) | Group of candidates appear only in those cells in unit; eliminate other candidates from those cells. Inverse of naked subsets. |
| **XY-Wing**          | Operation on unknowns (eliminate candidates) | Triple (3 cells in chain) | Chain (bivalue cells connected) | Pivot cell (XY) linked to two wings (XZ, YZ); eliminates Z where wings "see" it. Simple chain strategy. |
| **XYZ-Wing**         | Operation on unknowns (eliminate candidates) | Triple (3 cells, pivot has 3 candidates) | Chain (trivalue pivot + bivalue wings) | Extension of XY-Wing; pivot (XYZ) + wings (XZ, YZ); eliminates Z in common peer cells. |
| **X-Wing**           | Operation on unknowns (eliminate candidates) | Quad (4 cells in rectangle) | Grid-wide (2 rows + 2 cols) | Candidate in 2 rows only at 2 cols each, forming rectangle; eliminate from those cols elsewhere. Basic "fish" pattern. |
| **Swordfish**        | Operation on unknowns (eliminate candidates) | 9 cells (3x3 grid) | Grid-wide (3 rows + 3 cols) | Like X-Wing but for 3 rows/cols; eliminates in aligned cols/rows. Advanced fish. |
| **Coloring**         | Operation on unknowns (eliminate) or certainty (if contradiction) | Variable (chain length) | Chain (candidate graph) | Treat candidates as graph nodes, color chains; if same color sees each other, eliminate. Handles complex implications. |
| **Forcing Chain**    | Operation on unknowns (eliminate) or certainty (fill if all paths lead to same) | Variable (chain length) | Chain (implications across grid) | Follow "if A then B then C" chains; if contradiction or forced value, act. Can be short (nice loops) or long. |
| **Nishio**           | Operation on unknowns (eliminate via trial) | Variable (assumption + chain) | Trial/chain (assume candidate true/false) | Assume a candidate is true, propagate; if contradiction, eliminate it. Lightweight backtracking/trial-and-error. |

**Overall Patterns**:
- **Certainty vs. Unknowns**: Singles always fill (certainty). Most others eliminate (reducing unknowns), which may indirectly create new singles. Chains/trials can do both.
- **Single/Double/Triple**: Singles are "single," subsets scale to quad, wings/fish are fixed-size patterns (triple/quad+), chains are variable (often >3).
- **Human-Like Progression**: Humans start with singles (obvious fills), then subsets/intersections (local patterns), then fish/wings (grid scans), and chains/trials last (deductive reasoning). Your solver should apply in this order to generate natural sequences.
- **Implementation Tip**: All rely on candidates array. Simpler ones (singles/subsets) are unit-based and fast; chains are slower (graph traversal), so apply sparingly.

==================================================

And looking at this discussion with an AI about fish strategies here:

### Understanding Fish Strategies in Sudoku

Fish strategies are a family of advanced Sudoku solving techniques that focus on eliminating candidates based on patterns formed across multiple rows and columns (or vice versa). They are called "fish" because the patterns resemble fish shapes when diagrammed, with "fins" or extensions sometimes added in more complex variants. These strategies are particularly useful for medium to hard puzzles where simpler techniques like singles, subsets, or intersections don't make further progress.

At their core, fish strategies exploit alignments of candidates in a grid-wide manner. They operate on **candidates** (the possible numbers that could go in unsolved cells) and result in **eliminations** (removing candidates from cells), which can indirectly lead to fills via naked singles or other follow-on deductions. They don't directly fill cells but reduce possibilities.

Fish strategies are parameterized by size:
- **X-Wing**: The smallest and most common, for size 2 (like a 2x2 rectangle).
- **Swordfish**: For size 3 (a 3x3 pattern).
- Higher-order ones like Jellyfish (size 4) exist but are rarer and more computationally intensive; your solver plan focuses on X-Wing and Swordfish, which cover most cases.

These can be applied in two orientations:
- **Row-based**: Looking at candidates in rows that align to specific columns.
- **Column-based**: The symmetric case, swapping rows and columns.

I'll explain each in detail, starting with the general principle, then specifics for X-Wing and Swordfish. Since your context is implementing this in `fish.py`, I'll include implementation notes tied to a typical Sudoku solver setup (e.g., using a 9x9 grid and a candidates structure like a list of sets per cell).

#### General Principle of Fish Strategies
For a candidate number **k** (1-9):
1. **Scan for limited occurrences**: Identify a set of **n** rows where **k** appears as a candidate in exactly **n** columns across those rows (and no more).
2. **Check alignment**: Those occurrences must be confined to the same **n** columns. In other words, in those n rows, **k** only shows up in those n columns, forming a "base" pattern.
3. **Eliminate elsewhere**: Because **k** is "locked" to those n columns in the n rows, it means that in those n columns, **k** **cannot** appear in the other (9-n) rows—otherwise, it would violate Sudoku rules (no duplicates in columns). Thus, eliminate **k** from any cells in those n columns that are outside the n base rows.
4. **Symmetry**: Repeat the process swapping rows and columns (column-based fish).

This is efficient because it scans the entire grid but focuses on one candidate at a time. "Fins" can extend this (e.g., extra candidates outside the base that don't break the pattern but allow more eliminations), but basic implementations start without them.

Key benefits:
- Human-like: Solvers (and humans) spot these by scanning rows/columns for patterns, often after marking candidates.
- Efficiency: In code, it's O(1) per candidate (since grid is fixed 9x9), but you compute candidates first.

#### X-Wing: Detailed Explanation
X-Wing is the size-2 fish, named for the "X" shape formed by the four cells (like the wings of an X-wing fighter).

**How it Works (Step-by-Step)**:
1. **Select a candidate k**: Loop over each possible k (1-9).
2. **Build row candidate positions**: For each row (0-8), collect the list of columns where k is a candidate (i.e., unsolved cells in that row where k is possible).
3. **Find base rows**: Look for exactly two rows where the candidate positions for k are **exactly the same two columns**. For example:
   - Row 1: k possible only in columns 3 and 7.
   - Row 5: k possible only in columns 3 and 7.
   These two rows form the "base," and columns 3 and 7 are the "cover."
4. **Validate no extras**: Ensure that in these base rows, k doesn't appear elsewhere (already checked by the "exactly two" positions).
5. **Eliminate**: In columns 3 and 7, remove k from all other rows (except rows 1 and 5). Why? Because if k were in, say, row 2 column 3, then:
   - Row 1's k must go in column 7 (since column 3 is taken).
   - Row 5's k must go in column 3 or 7, but this creates conflicts in the columns.
   Essentially, the pattern forces k to be placed in the four cells (row1-col3, row1-col7, row5-col3, row5-col7) like a rectangle, and Sudoku forbids k duplicates in columns, so no other k in those columns.
6. **Check boxes**: Importantly, these positions shouldn't all be in the same box (subgrid), as that might be handled by simpler techniques, but X-Wing works across boxes.
7. **Column-based variant**: Repeat by transposing: Find two columns where k is only in the same two rows, then eliminate k from those rows in other columns.

**Example**:
Imagine a grid where candidate 5 is possible in:
- Row 2: Columns 1 and 4.
- Row 7: Columns 1 and 4.
- And elsewhere in columns 1 and 4, but not in rows 2 or 7.

This is an X-Wing on rows 2/7, columns 1/4. Eliminate 5 from all other cells in columns 1 and 4 (e.g., row 0 col 1, row 3 col 4, etc.).

**Visual**:
```
Columns: 1   4
Row 2:   [5] [5]
Row 7:   [5] [5]
```
The "X" connects the diagonals, implying eliminations vertically.

**Implementation Notes for `fish.py`**:
- Use a candidates structure: e.g., `candidates[row][col]` = set of possible numbers (or a 9x9x9 boolean array for speed).
- Function signature: `find_x_wing(candidates: list[list[set]]) -> list[dict]`, where each dict is a deduction like `{'type': 'eliminate', 'candidate': k, 'row': r, 'col': c}`.
- Steps in code:
  - For k in 1..9:
    - row_positions = [[] for _ in range(9)]  # list of cols where k is candidate in each row
    - For r in 0..8:
      for c in 0..8:
        if unsolved(r,c) and k in candidates[r][c]:
          row_positions[r].append(c)
    - Now, find pairs of rows where len(row_positions[r1]) == 2, len(row_positions[r2]) == 2, and set(row_positions[r1]) == set(row_positions[r2]).
    - For each such pair (r1, r2), cols = row_positions[r1]
    - For each col in cols:
      for other_r not in [r1, r2]:
        if k in candidates[other_r][col]:
          add deduction: eliminate k from (other_r, col)
- Do the same for column-based (transpose the logic: col_positions = [[] for _ in range(9)], etc.).
- Edge cases: Ignore if positions are in same box, or if no eliminations possible. Also, ensure the two rows aren't the same.
- Integrate: In `strategies.py`, add to STRATEGY_FUNCTIONS, call in solver loop after simpler strategies.

This should be straightforward and fast; test on puzzles where X-Wing is needed (e.g., from your dataset's medium levels).

#### Swordfish: Detailed Explanation
Swordfish is the size-3 fish, extending X-Wing to three rows and three columns. It's rarer but powerful for harder puzzles.

**How it Works (Step-by-Step)**:
1. **Select a candidate k**: Same as above.
2. **Build row candidate positions**: For each row, list columns where k is a candidate, but now look for rows where k appears in **at most 3 columns** (ideally exactly 3, but allowing 2 for "degenerate" cases).
3. **Find base rows**: Identify a combination of three rows where the **union** of their candidate columns for k has **exactly 3 columns**, and each row has k in at least two of those columns (to ensure coverage). More precisely:
   - The total unique columns across the three rows <= 3.
   - But each of the three columns must be "covered" by at least two rows (though basic Swordfish requires exact alignment).
   Standard definition: Find three rows where k appears only in the same three columns (each row has k in up to those three cols).
4. **Eliminate**: In those three columns, remove k from all rows outside the three base rows. The logic is analogous: The pattern forces k's placements in those columns to be confined to the base rows, preventing duplicates.
5. **Column-based**: Symmetric, find three columns with k only in the same three rows, eliminate from other columns in those rows.

**Example**:
Suppose candidate 4 in:
- Row 0: Columns 2, 5
- Row 3: Columns 2, 5, 8
- Row 6: Columns 5, 8
The union is columns 2,5,8 (exactly 3), and occurrences are within them. This is a Swordfish; eliminate 4 from other rows in columns 2,5,8.

**Visual**:
```
Columns: 2   5   8
Row 0:   [4] [4] 
Row 3:   [4] [4] [4]
Row 6:        [4] [4]
```
The "fish" shape connects the positions; eliminations are vertical in those columns.

**Implementation Notes for `fish.py`**:
- Similar to X-Wing, but generalize to n=3.
- For better modularity, write a generic `find_fish(candidates, n=2 or 3)`:
  - Use combinations from itertools: for base_rows in combinations(range(9), n):
    - Collect union_cols = set()
    - For r in base_rows:
      cols_for_r = [c for c in range(9) if k in candidates[r][c]]
      if len(cols_for_r) > n: skip
      union_cols.update(cols_for_r)
    - If len(union_cols) == n:
      - Check coverage: For each col in union_cols, count how many base_rows have k in that col; should be at least 2 (for strong links).
      - If valid, eliminate k from other_rows in union_cols where present.
- This handles both X-Wing (n=2) and Swordfish (n=3) in one function.
- Optimizations: Skip if union_cols > n early. For n=3, it's more combinatorial (C(9,3)=84), but still fast.
- Testing: Use puzzles requiring Swordfish; validate no false eliminations (e.g., run is_valid_sudoku after).

#### Generic Pattern-Scanning Helper
As per your plan, add a helper in `fish.py` for scanning: e.g., `scan_for_fish(candidates, k, n, is_row_based=True)` that returns potential bases and covers. This makes it extensible (e.g., to Jellyfish n=4 later).

#### Integration into Solver
- In `solver.py`: After computing candidates, call `find_fish_deductions` in the strategy loop, after intersections/subsets.
- Update `utils.apply_deductions`: Ensure it handles eliminations by removing from candidates and checking for new singles.
- Record steps: Each elimination batch as a step dict with strategy='fish', subtype='x-wing' or 'swordfish', affected cells.
- Testing: Create unit tests with minimal grids (e.g., almost solved but with one fish pattern), confirm eliminations lead to progress without conflicts.

This should complete your fish implementation, enabling the solver to tackle harder puzzles with human-like pattern recognition. If you need code snippets or examples from your dataset, let me know!

======================================================

MAIN INSTRUCTIONS HERE:

ENABLE ELIMINATION HANDLING

Extend utils.apply_deductions (and/or a candidate-management helper) so elimination-type deductions can update candidates immediately, allowing advanced strategies to propagate their effects.

IMPLEMENT FISH STRATEGIES

Fish strategies (fish.py): X-Wing and Swordfish with a generic pattern-scanning helper.

KEY DETAILS

THE NEW IMPLEMENTATIONS MUST MATCH OR UPDATE CURRENT API SO THAT OPERATIONS CAN REMAIN HIGH SPEED VECTORIZED. HERE IS A POSSIBLE METHOD:

You are an expert Python developer specializing in vectorized NumPy implementations for batch processing, particularly for Sudoku solvers. Your task is to implement the fish strategies (X-Wing and Swordfish) in a new file called `fish.py`, ensuring they integrate holistically into the existing Sudoku solver codebase. The goal is to match the style, methods, and API of the existing strategies (from `singles.py`, `subsets.py`, and `intersections.py`) as closely as possible, while being flexible to update the overall API where bending the fish implementation to fit the original would be inelegant or inefficient. Prioritize clean, maintainable code that supports batch processing over N puzzles, uses NumPy for vectorization, and minimizes loops to small fixed sizes (e.g., 9 rows/cols/values, 3 boxes).

### Key Principles for Matching and Integration:
- **API Matching**: All strategy functions take `candidates: np.ndarray` (shape `(N, 9, 9, 9)` boolean, where last dim is for values 1-9) and `all_deductions: list[list[dict]]` (list per puzzle, append dicts in-place). Return None. Use `np` operations like `np.sum`, `np.any`, `np.where` for vectorization, similar to how singles use masks (e.g., `cell_counts = np.sum(candidates, axis=3) == 1`) and subsets use `combinations` per unit.
- **Deductions Format**: Match existing formats exactly. For eliminations (fish are elimination-only, like subsets/intersections): `{'type': 'x_wing_row' or 'swordfish_col', 'positions': list of (r,c) tuples for the base pattern, 'candidate': int (the value k), 'eliminations': list of [((r,c), [candidates_to_elim])]}`. Include pattern details like `'base_rows': list[int]`, `'cover_cols': list[int]` for clarity, similar to `'box': (br,bc)` in intersections.
- **Vectorization Style**: Hybrid like subsets (vectorized over batch/N, loops over 9/3/k/combos). Use bitmasks for column sets (e.g., `row_bitmasks = np.sum(cand_k * (1 << np.arange(9))[None, None, :], axis=2)`) to efficiently compute unions and counts, as this is elegant for fish patterns without overcomplicating.
- **Variants**: Fish need row-based and column-based (symmetric). Implement as separate functions or a generic one with a param, but prefer explicit variants like `_row`/`_col` to match hidden singles (`_row`/`_col`/`_box`) and intersections (`_row`/`_col`).
- **Flexibility for API Updates**: If exact matching is awkward (e.g., fish combos are more combinatorial than singles), update shared parts like `apply_deductions` in `utils.py` to handle eliminations by mutating `candidates` (e.g., `candidates[n, r, c, val-1] = False` for each elim). Also, update `strategies.py` to group fish (e.g., `'fish': ['x_wing_row', 'x_wing_col', ...]`). In `solver.py`, add to default `strategies` list after intersections for escalation order.
- **Holistic Integration**: Ensure fish propagates effects (eliminations create new singles/subsets). Update the solver loop in `solver.py` to recompute candidates after applying eliminations if needed. Test for no conflicts using `is_valid`. Make sure `main.py` and sequence display handle new types (e.g., format fish in `format_deduction`).
- **Implementation Details**:
  - **Candidates Handling**: Extract `cand_k = candidates[..., k-1]` for each k=1-9, vectorized.
  - **Bitmasks and Popcount**: Use bitmasks for row/column positions (efficient for unions via `np.bitwise_or.reduce`). For popcount, use `np.popcount` if available, else a vectorized alternative like `np.array([bin(x).count('1') for x in union_bits])`.
  - **Combinations**: Use `itertools.combinations(range(9), n)` for base rows/cols (n=2 for X-Wing, 3 for Swordfish), check union count == n and each base has <=n positions >0.
  - **Coverage**: Optionally ensure each cover col appears in >=2 bases for strong links, but start with basic.
  - **Column-Based**: Duplicate logic with `candidates.swapaxes(1,2)`, adjust types/keys accordingly.
  - **Edge Cases**: Skip if no elims, ignore same-box patterns (handled by simpler strategies), ensure unsolved cells only.
  - **Updates to Other Files**:
    - `strategies.py`: Add to `STRATEGY_FUNCTIONS` (e.g., `'x_wing_row': find_x_wing_rows, ...`). Expand groups like `'fish'` in `find_deductions_batch`.
    - `utils.py`: Extend `apply_deductions` to loop over eliminations and mutate candidates (pass candidates as arg). Update `format_deduction` for fish types.
    - `solver.py`: In `solve_batch`, after `apply_deductions`, recompute candidates if elims applied. Add fish to `strategies` list.
    - `README.md`: Update "Implemented Strategies" with fish.

### Output Requirements:
- Provide the full code for `fish.py`.
- Provide diffs or full updated code for modified files (`strategies.py`, `utils.py`, `solver.py`).
- Include a brief explanation of changes and why they match/update the API.
- Ensure the implementation is performant for large batches (e.g., dataset's ~4M puzzles).
======================================================

GO. IMPLEMENT MAIN INSTRUCTIONS.