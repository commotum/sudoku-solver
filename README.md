## Sudoku Solver

Human-style Sudoku solver that generates step-by-step solving sequences. It downloads a large dataset, buckets puzzles by difficulty, and applies modular strategies (singles, subsets, intersections, and more) to produce human-like deductions and sequences.

### Features
- **Human-like strategy engine**: Starts with singles; extendable to subsets, intersections, fish, wings, and chains.
- **Batch-first design**: Vectorized candidate computation across puzzles.
- **Reproducible sampling**: Daily deterministic selection in `main.py` for a random puzzle.
- **Dataset pipeline**: Downloads from Hugging Face and saves grouped `.npy` files per difficulty.

---

## Setup
- **Python**: 3.9+ recommended
- **Create env and install**:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- **Requirements** (from `requirements.txt`): `numpy`, `huggingface_hub`, `tqdm`

## Download and Prepare Data
This project uses the `sapientinc/sudoku-extreme` dataset on Hugging Face and saves per-difficulty buckets as NumPy arrays.

- Generate processed files:
```bash
python dataset_download.py
```
- Output directory: `data/sudoku-extreme-processed/`
- Files created per difficulty level `L`:
  - `lvl-L-inputs.npy` (shape: `(N, 9, 9)`)
  - `lvl-L-outputs.npy` (shape: `(N, 9, 9)`)

## Quickstart
Run the daily random puzzle (level 0) and print the step-by-step sequence:
```bash
python main.py
```
This selects a reproducible puzzle index (seeded by today’s date), solves it with human strategies, and prints each step with deductions.

### Solve a batch for a specific difficulty
Use the programmatic API to load and solve a difficulty bucket:
```python
import numpy as np
from solver import load_and_solve_difficulty

# Solve level 10, optionally subsample the first 100 puzzles
sequences = load_and_solve_difficulty(10, data_dir="data/sudoku-extreme-processed", subsample=100)

# sequences is a List[List[Dict]] where each inner list is a puzzle's step-by-step sequence
print(len(sequences), "puzzles solved")
```

---

## How it Works
- `dataset_download.py`: Downloads CSVs from the HF dataset, converts to 9x9 arrays, groups by difficulty, and writes `.npy` files.
- `solver.py`:
  - `solve_batch(inputs, outputs, max_steps=100, verbose=False)`: Human-style loop that records sequences of steps. At each step it:
    - Computes candidates (vectorized)
    - Runs selected strategies via `strategies.find_deductions_batch`
    - Applies fills (certainties) and records all deductions
  - `load_and_solve_difficulty(diff, data_dir, subsample=None)`: Loads level buckets and solves them.
- `strategies/strategies.py`: Central hub that imports strategy functions and maps names → functions in `STRATEGY_FUNCTIONS`. Also expands grouped names like `hidden_single` into row/col/box variants.
- `utils.py`: Validation (`is_solved`, `is_valid`), application of deductions (`apply_deductions`), and a grid pretty-printer.

### Current default strategies used in the loop
In `solver.solve_batch`, the default list is:
```python
strategies = ["naked_single", "hidden_single"]
```
You can expand this list (see Implemented Strategies below) to include subsets and intersections once you’re ready to apply eliminations in addition to fills.

---

## Strategy Taxonomy
Strategies are organized by action type, complexity, and scope. The solver should apply simpler methods first for natural, human-like progress.

| Strategy | Action Type | Complexity/Size | Scope | Notes |
|---|---|---|---|---|
| Naked Single | Certainty (fill cell) | Single (1 candidate in cell) | Cell-only | Simplest. Applied first. |
| Hidden Single | Certainty (fill cell) | Single (1 cell for a candidate in unit) | Unit (row/col/box) | Only one place in the unit fits a candidate. |
| Locked Candidates | Operation on unknowns (eliminate) | Pair/Triple | Intersection (box↔row/col) | Pointing/Claiming eliminations. |
| Naked Pair/Triplet/Quad | Operation on unknowns (eliminate) | Pair/Triple/Quad | Unit (row/col/box) | Reduce other cells in unit. |
| Hidden Pair/Triplet/Quad | Operation on unknowns (eliminate) | Pair/Triple/Quad | Unit (row/col/box) | Inverse of naked subsets. |
| XY-Wing | Operation on unknowns (eliminate) | Triple (3 cells) | Chain | Bivalue pivot with two wings. |
| XYZ-Wing | Operation on unknowns (eliminate) | Triple (3 cells) | Chain | Trivalue pivot + two wings. |
| X-Wing | Operation on unknowns (eliminate) | Quad (4-cell rectangle) | Grid-wide | Row/col rectangle pattern. |
| Swordfish | Operation on unknowns (eliminate) | 9 cells (3×3) | Grid-wide | 3 rows × 3 cols alignment. |
| Coloring | Eliminate or certainty | Variable | Chain | Candidate graph coloring. |
| Forcing Chain | Eliminate or certainty | Variable | Chain | Implication chains; nice loops. |
| Nishio | Eliminate via trial | Variable | Trial/chain | Assume and propagate until contradiction. |

### Implemented strategies (code today)
- **Singles** (`strategies/singles.py`):
  - `naked_single`
  - `hidden_single_row`, `hidden_single_col`, `hidden_single_box` (group name: `hidden_single`)
- **Subsets** (`strategies/subsets.py`):
  - `naked_subsets` (pairs/triplets/quads; row/col/box)
  - `hidden_subsets` (pairs/triplets/quads; row/col/box)
- **Intersections** (`strategies/intersections.py`):
  - `locked_pointing` (row/col variants)
  - `locked_claiming` (row/col variants)

All implemented strategy functions are wired via `strategies/strategies.py` and callable through:
```python
from strategies import find_deductions_batch
# Example: expand grouped names like 'hidden_single', 'subsets', 'intersections'
deductions_per_puzzle = find_deductions_batch(grids, strategies=[
    "naked_single",
    "hidden_single",
    "subsets",
    "intersections",
])
```
Note: `utils.apply_deductions` currently applies only certainty-type fills (e.g., singles). Elimination-type deductions are recorded but not yet applied to candidates directly. Extend `apply_deductions` to mutate candidate state if you want eliminations to propagate within the same step.

---

## Outputs: Sequences
Each puzzle’s solution is a sequence of step records:
- `{"step": i, "grid_state": List[int], "deductions": List[Dict]}`
- `grid_state` is a flat 81-length snapshot after the step
- `deductions` contains items like:
  - Singles: `{ "type": "naked_single", "position": (r, c), "value": v }`
  - Eliminations: `{ "type": "locked_pointing_row", "eliminations": [ ((r, c), [values...]), ... ] }`

You can save these sequences for ML or analysis.

---

## Project Structure
- `dataset_download.py`: Download + bucket dataset into `.npy` files
- `main.py`: Daily random demo; prints the solving sequence for one puzzle
- `solver.py`: Batch solver + difficulty loader API
- `strategies/`:
  - `strategies.py`: Strategy registry + grouped names expansion + batch deduction driver
  - `singles.py`, `subsets.py`, `intersections.py`: Implemented strategy families
  - `fish.py`, `wings.py`, `chains.py`: Placeholders for advanced strategies as you extend
- `utils.py`: Validation, application of deductions (fills), pretty printing
- `data/`: Generated `.npy` files per difficulty level

---

## Extending
- Add a new strategy in an existing family (or create a new module), export a function with signature:
  - `fn(candidates: np.ndarray, all_deductions: list[list[dict]]) -> None`
- Register it in `STRATEGY_FUNCTIONS` in `strategies/strategies.py`.
- Include it in the `strategies` list passed to `find_deductions_batch` and in `solver.solve_batch`.
- Update `utils.apply_deductions` if the new strategy performs eliminations that should affect subsequent steps.

## License
MIT (or your preferred license).
