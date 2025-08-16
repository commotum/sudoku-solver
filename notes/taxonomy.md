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



∴   Therefore
∵   Because
∄   There Does Not Exist
∁   Complement
𝍸   Tally
∈   Element of; indicates membership in a set.
∉   Not an element of; indicates non-membership.

±   
∑
÷
∞
∅   Empty set; a set with no elements.
∩   Intersection; common elements between sets.
∪   Union; combines elements from sets.
⊆   Subset of or equal to; all elements of one set are in another.

+/−/=/</>

?𝍸4

| Symbol | Unicode | Meaning                                                   |
|:------:|:-------:|:---------------------------------------------------------:|
|   =    | U+003D  | Equality; two expressions have the same value.            |
|   ≠    | U+2260  | Inequality; two expressions differ in value.              |
|   <    | U+003C  | Less than; one value smaller than another.                |
|   >    | U+003E  | Greater than; one value larger than another.              |
|   ≤    | U+2264  | Less than or equal to; inclusive lower bound.             |
|   ≥    | U+2265  | Greater than or equal to; inclusive upper bound.          |
|   ≈    | U+2248  | Approximately equal; values close but not identical.      |
|   ≡    | U+2261  | Congruent; strong equivalence or identical nature.        |
|   ∁    | U+2201  | Complement; elements not in the original set.             |
|   ∵    | U+2235  | Because; indicates reason in logical arguments.           |
|   ∴    | U+2234  | Therefore; indicates conclusion in logical arguments.     |
|   ∄    | U+2204  | Does not exist; negated existential quantifier.           |
|   ∃    | U+2203  | There exists; existential quantifier in logic.            |
|   ∌    | U+220C  | Does not contain; negated set membership.                 |
|   ∋    | U+220B  | Contains member; reverse set membership relation.         |
|   +    | U+002B  | Addition; sum of two or more values.                      |
|   −    | U+2212  | Subtraction; difference between two values.               |
|   ×    | U+00D7  | Multiplication; product of two values.                    |
|   ÷    | U+00F7  | Division; quotient of two values.                         |
|   ∑    | U+2211  | Summation; total of a series of terms.                    |
|   ∞    | U+221E  | Infinity; unbounded or limitless quantity.                |
|   ±    | U+00B1  | Plus-minus; indicates range or alternatives.              |
|   ∈    | U+2208  | Element of; membership in a set.                          |
|   ∉    | U+2209  | Not element of; non-membership in set.                    |
|   ⊆    | U+2286  | Subset equal; all elements included in another.           |
|   ∪    | U+222A  | Union; combines elements from multiple sets.              |
|   ∩    | U+2229  | Intersection; common elements in sets.                    |
|   ∅    | U+2205  | Empty set; set with no elements.                          |
|   ∀    | U+2200  | For all; universal quantifier in logic.                   |
|   ∃    | U+2203  | There exists; existential quantifier in logic.            |
|   ¬    | U+00AC  | Negation; inverts truth value of operand.                 |
|   ∧    | U+2227  | Conjunction; true if both operands true.                  |
|   ∨    | U+2228  | Disjunction; true if at least one operand true.           |
|   ⊕    | U+2295  | Exclusive or; true if exactly one operand true.           |
|   ⇒    | U+21D2  | Implication; false only if antecedent T and consequent F. |
|   ⇔    | U+21D4  | Biconditional; true if operands match in truth.           |
|   ⊤    | U+22A4  | Tautology; always true proposition.                       |
|   ⊥    | U+22A5  | Contradiction; always false proposition.                  |
|   ⊢    | U+22A2  | Proves; syntactic entailment from axioms.                 |


ASSIGN, EXCLUDE, ASSUME
ASSERT, REJECT, PROPOSE

R2C8 = 8
R2C8 ≠ 8
R2C8 = -8
R2C8 ≠ -8


 T-8:  Δ +4

 T = 8
 Δ = +4


[ROW ID, COLUMN ID, ACTION ID, VALUE ID]

IS ROW 8 COLUMN 2 EQUAL TO 3?

? R8C2 = 3 : 

Which numbers are in block 1?

? ∋ B1 (Returns B1 Placements)
? ∌ B1 (Returns B1 Absences)

? ∋ C1
? ∌ C1

∋ C1 = ?
∌ C1 ≠ ?


allowed symbols?

Is board valid?



Glossary:

REGION:
A set or collection of positions (cells) on the Sudoku board. Regions are subsets of the board's positions, varying in size and structure, and serve as foundational units for constraints and puzzle structure. All regions are disjoint or overlapping collections of positions, but core gameplay constraints (e.g., uniqueness of digits 1–9) apply specifically to certain region types.

    REGION:SQUARE
        The atomic (smallest indivisible) region. A singleton set consisting of exactly one position, which may hold a given digit (1–9) or a set of candidate digits during solving.

    REGION:HOUSE
        An intermediate region consisting of exactly nine positions, where the digits 1–9 must each appear exactly once (the core uniqueness constraint of Sudoku). Houses form the primary partitioning of the board into constraint-bearing groups and are categorized into three subtypes based on their geometric arrangement.

        REGION:HOUSE:ROW
            A horizontal house: the set of nine positions sharing the same row index (typically denoted as rows 1–9 from top to bottom).

        REGION:HOUSE:COLUMN
            A vertical house: the set of nine positions sharing the same column index (typically denoted as columns 1–9 from left to right).

        REGION:HOUSE:BOX
            A block house: the set of nine positions forming a 3×3 subgrid (typically denoted as boxes 1–9, arranged in a 3×3 meta-grid from top-left to bottom-right).

    REGION:BOARD
        The maximal (universal) region: the complete set of 81 positions, arranged in a 9×9 grid subdivided into 9 rows, 9 columns, and 9 boxes. The board is the union of all houses and the domain over which the puzzle is defined and solved.

REGION:BAND
    A horizontal meta-region (also called a "chute" in some contexts) consisting of exactly 27 positions, formed by three consecutive rows (thus encompassing three full houses of the row subtype and one horizontal row of three 3×3 boxes). Bands partition the board into three non-overlapping horizontal strips (typically labeled 1–3 from top to bottom) and are used in puzzle structure, variant rules, and advanced solving techniques (e.g., band-based patterns or symmetries).

REGION:STACK
    A vertical meta-region (also called a "chute" in some contexts) consisting of exactly 27 positions, formed by three consecutive columns (thus encompassing three full houses of the column subtype and one vertical column of three 3×3 boxes). Stacks partition the board into three non-overlapping vertical strips (typically labeled 1–3 from left to right) and are used analogously to bands in puzzle structure, variant rules, and advanced solving techniques (e.g., stack-based patterns or symmetries).


A denoted position that holds either a forced/known value or a set of candidates.
BOARD - Place 2, A collection of SQUARES arranged in a 9x9 grid containing initial values and empty cells
ROW
COLUMN
BOX
HOUSE
BAND
STACK


ASSIGN - Action 1, Filling an unfilled square with a Forced Value
EXCLUDE - Action 2, Removing a value from an unfilled squares candidate set
ASSUME - The act of filling an unfilled square with an uncertain value
ADVANCE - 

BOARD - Space 1, dimensions 9x9, contains initial values and placed values
HOUSE — any row, column, or box.
ROW - horizontal 
COLUMN - 

Contradiction – In Sudoku an illegal and therefore contradictory situation can occur if a) there are no candidates left in a cell, or b) two or more cells claim to be true. The aim of many strategies is to show a contradiction.



---

Notes:

> The first thing to consider about the way a human being tackles the problem is
> that a puzzle is never submitted in a purely logical form; on the contrary, it is always
> centred on a spatial presentation[^2], i.e.: "complete the following grid…".
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Prologue**, p. 14.

[^2]: Notice that the same remark applies to most of the so called logical games.

```bibtex
@book{berthier2007hiddenlogic,
  author    = {Denis Berthier},
  title     = {The Hidden Logic of Sudoku},
  edition   = {2nd},
  year      = {2007},
  isbn      = {978-1-84799-214-7}
}
```

---

> In every cell, one writes either the number that must definitely occupy it or (with a pencil and in smaller size) the list of all its "candidates", i.e. of all the numbers that may still occupy it. Solving the grid then consists of progressively reducing this list of candidates by constraints propagation, until only one possibility remains for each cell.
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Prologue**, pp. 14–15.

---

> This universal spatial presentation of the puzzle, together with the associated model of cells to be filled with one number each, hide some logical symmetries of the problem. And considering that eliciting these symmetries leads to the quasi identification of complex rules (such as X-Wing, Swordfish and Jellyfish) with apparently much simpler ones (such as Naked Pairs, Naked Triplets and Naked Quadruplets respectively), there is a mathematical beauty in it.
>
> As everybody knows, the Powers of Darkness do not like Beauty.
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Prologue**, p. 15.

---

> One vicious thing leading to a virtuous one, the whole process ended with this book
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Prologue**, p. 15.

---

> **1.1. Statement of the Sudoku problem**  
> Given a 9x9 grid, partially filled with numbers from 1 to 9 (the "entries" of the
> problem, also called the "clues" or the "givens"), complete it with numbers from 1 to
> 9 so that in every of the nine rows, in every of the nine columns and in every of the
> nine disjoint blocks of 3x3 contiguous cells, the following property holds:
> – there is at most one occurrence of each of these numbers.
>
> …
>
> Since rows, columns and blocks play similar roles in the defining constraints,
> they will naturally appear to do so in many other places and it is convenient to introduce a word that makes no difference between them: a unit is either a row or a
> column or a block. And we say that two cells share a unit if they are either in the
> same row or in the same column or in the same block (where "or" is non exclusive).
> We also say that these two cells are linked, or that they see each other. It should be
> noticed that this (symmetric) relation between two cells, whichever of the three
> equivalent names it is given, does not depend in any way on the content of these
> cells but only on their place in the grid; it is therefore a straightforward and quasi
> physical notion.
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Introduction**, p. 17.

---

> Figure 1 below shows the standard presentations of a problem grid (also called a
> puzzle) and of a solution grid (also called a complete Sudoku grid).
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Introduction**, p. 18.

---

> The process of solving a grid "by hand" is generally initialised
> by defining the "candidates" for each cell. For later formalisation, one must give a
> careful definition of this notion: at any stage of the resolution process, candidates
> for a cell are the numbers that are not yet explicitly known to be impossible values
> for this cell.
>
> — Denis Berthier, *The Hidden Logic of Sudoku*, 2nd ed., **Introduction**, p. 19.
