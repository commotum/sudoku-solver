# Sudoku Solver — Human‑Style, Strategy‑First

A human‑style Sudoku solver that generates step‑by‑step solving sequences. It downloads a large dataset, buckets puzzles by difficulty, and applies modular strategies (singles, subsets, intersections, and more) to produce human‑like deductions.

---

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Data: Download & Prepare](#data-download--prepare)
* [Quickstart](#quickstart)
* [How It Works](#how-it-works)

  * [Default Strategies](#default-strategies)
  * [Strategy Taxonomy](#strategy-taxonomy)
  * [Implemented Strategies (today)](#implemented-strategies-today)
* [Outputs: Sequences](#outputs-sequences)
* [Project Structure](#project-structure)
* [Extending](#extending)
* [Dataset & Citations](#dataset--citations)

  * [Dataset: Hardest Sudoku Puzzle Dataset V2](#dataset-hardest-sudoku-puzzle-dataset-v2)
  * [Paper: Hierarchical Reasoning Model (HRM)](#paper-hierarchical-reasoning-model-hrm)
* [License](#license)
* [Acknowledgements](#acknowledgements)

---

## Features

* **Human‑like strategy engine**: Starts with singles; extendable to subsets, intersections, fish, wings, and chains.
* **Batch‑first design**: Vectorized candidate computation across puzzles.
* **Reproducible sampling**: Daily deterministic selection in `main.py` for a random puzzle.
* **Dataset pipeline**: Downloads from Hugging Face and saves grouped `.npy` files per difficulty.

---

## Installation

* **Python**: 3.9+ recommended
* **Create env and install**:

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
* **Requirements** (from `requirements.txt`): `numpy`, `huggingface_hub`, `tqdm`

---

## Data: Download & Prepare

This project uses the **`sapientinc/sudoku-extreme`** dataset on Hugging Face and saves per‑difficulty buckets as NumPy arrays.

* Generate processed files:

  ```bash
  python dataset_download.py
  ```
* Output directory: `data/sudoku-extreme-processed/`
* Files created per difficulty level `L`:

  * `lvl-L-inputs.npy` (shape: `(N, 9, 9)`)
  * `lvl-L-outputs.npy` (shape: `(N, 9, 9)`)

> The download script uses `hf_hub_download` with `repo_type="dataset"` and reads `train.csv` and `test.csv`. Ratings are preserved so puzzles can be bucketed by difficulty.

---

## Quickstart

Run the daily random puzzle (level 0) and print the step‑by‑step sequence:

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

## How It Works

* **`dataset_download.py`**: Downloads CSVs from the HF dataset, converts to 9×9 arrays, groups by difficulty, and writes `.npy` files.
* **`solver.py`**:

  * `solve_batch(inputs, outputs, max_steps=100, verbose=False)`: Human‑style loop that records sequences of steps. At each step it:

    * Computes candidates (vectorized)
    * Runs selected strategies via `strategies.find_deductions_batch`
    * Applies fills (certainties) and records all deductions
  * `load_and_solve_difficulty(diff, data_dir, subsample=None)`: Loads level buckets and solves them.
* **`strategies/strategies.py`**: Central hub that imports strategy functions and maps names → functions in `STRATEGY_FUNCTIONS`. Also expands grouped names like `hidden_single` into row/col/box variants.
* **`utils.py`**: Validation (`is_solved`, `is_valid`), application of deductions (`apply_deductions`), and a grid pretty‑printer.

### Default Strategies

In `solver.solve_batch`, the default list is:

```python
strategies = ["naked_single", "hidden_single"]
```

You can expand this list (see below) to include subsets and intersections once you’re ready to apply eliminations in addition to fills.

### Strategy Taxonomy

Strategies are organized by action type, complexity, and scope. The solver should apply simpler methods first for natural, human‑like progress.

| Strategy                 | Action Type                       | Complexity/Size                         | Scope                      | Notes                                        |
| ------------------------ | --------------------------------- | --------------------------------------- | -------------------------- | -------------------------------------------- |
| Naked Single             | Certainty (fill cell)             | Single (1 candidate in cell)            | Cell‑only                  | Simplest. Applied first.                     |
| Hidden Single            | Certainty (fill cell)             | Single (1 cell for a candidate in unit) | Unit (row/col/box)         | Only one place in the unit fits a candidate. |
| Locked Candidates        | Operation on unknowns (eliminate) | Pair/Triple                             | Intersection (box↔row/col) | Pointing/Claiming eliminations.              |
| Naked Pair/Triplet/Quad  | Operation on unknowns (eliminate) | Pair/Triple/Quad                        | Unit (row/col/box)         | Reduce other cells in unit.                  |
| Hidden Pair/Triplet/Quad | Operation on unknowns (eliminate) | Pair/Triple/Quad                        | Unit (row/col/box)         | Inverse of naked subsets.                    |
| XY‑Wing                  | Operation on unknowns (eliminate) | Triple (3 cells)                        | Chain                      | Bivalue pivot with two wings.                |
| XYZ‑Wing                 | Operation on unknowns (eliminate) | Triple (3 cells)                        | Chain                      | Trivalue pivot + two wings.                  |
| X‑Wing                   | Operation on unknowns (eliminate) | Quad (4‑cell rectangle)                 | Grid‑wide                  | Row/col rectangle pattern.                   |
| Swordfish                | Operation on unknowns (eliminate) | 9 cells (3×3)                           | Grid‑wide                  | 3 rows × 3 cols alignment.                   |
| Coloring                 | Eliminate or certainty            | Variable                                | Chain                      | Candidate graph coloring.                    |
| Forcing Chain            | Eliminate or certainty            | Variable                                | Chain                      | Implication chains; nice loops.              |
| Nishio                   | Eliminate via trial               | Variable                                | Trial/chain                | Assume and propagate until contradiction.    |

### Implemented Strategies (today)

* **Singles** (`strategies/singles.py`):

  * `naked_single`
  * `hidden_single_row`, `hidden_single_col`, `hidden_single_box` (group name: `hidden_single`)
* **Subsets** (`strategies/subsets.py`):

  * `naked_subsets` (pairs/triplets/quads; row/col/box)
  * `hidden_subsets` (pairs/triplets/quads; row/col/box)
* **Intersections** (`strategies/intersections.py`):

  * `locked_pointing` (row/col variants)
  * `locked_claiming` (row/col variants)

> Note: `utils.apply_deductions` currently applies only certainty‑type fills (e.g., singles). Elimination‑type deductions are recorded but not yet applied to candidates directly. Extend `apply_deductions` to mutate candidate state if you want eliminations to propagate within the same step.

---

## Outputs: Sequences

Each puzzle’s solution is a sequence of step records:

* `{"step": i, "grid_state": List[int], "deductions": List[Dict]}`
* `grid_state` is a flat 81‑length snapshot after the step
* `deductions` contains items like:

  * Singles: `{ "type": "naked_single", "position": (r, c), "value": v }`
  * Eliminations: `{ "type": "locked_pointing_row", "eliminations": [ ((r, c), [values...]), ... ] }`

You can save these sequences for ML or analysis.

---

## Project Structure

```
dataset_download.py        # Download + bucket dataset into .npy files
main.py                    # Daily random demo; prints the solving sequence for one puzzle
solver.py                  # Batch solver + difficulty loader API
strategies/
  strategies.py            # Strategy registry + grouped names expansion + batch deduction driver
  singles.py               # Singles
  subsets.py               # Naked/hidden subsets
  intersections.py         # Locked candidates (pointing/claiming)
  fish.py, wings.py, chains.py   # Placeholders for advanced strategies
utils.py                   # Validation, application of deductions (fills), pretty printing
data/                      # Generated .npy files per difficulty level
```

---

## Extending

* Add a new strategy in an existing family (or create a new module), export a function with signature:

  * `fn(candidates: np.ndarray, all_deductions: list[list[dict]]) -> None`
* Register it in `STRATEGY_FUNCTIONS` in `strategies/strategies.py`.
* Include it in the `strategies` list passed to `find_deductions_batch` and in `solver.solve_batch`.
* Update `utils.apply_deductions` if the new strategy performs eliminations that should affect subsequent steps.

---

## Dataset & Citations

### Dataset: Hardest Sudoku Puzzle Dataset V2

This project uses the **`sapientinc/sudoku-extreme`** dataset on Hugging Face.

* **Composition**: mixture of easy and very hard Sudoku puzzles collected from the community.
* **Splits & size**: Train `train.csv` (≈3.8M), Test `test.csv` (≈423k), **total** ≈4,254,780 rows.
* **Characteristics**: exact de‑duplication; each puzzle has a unique solution; train/test are mathematically inequivalent; **rating** = number of backtracks required by the `tdoku` solver (higher is harder).
* **Sources**: `tdoku` benchmarks and `enjoysudoku` community threads.

**Suggested dataset citation (BibTeX)**

```bibtex
@dataset{sapientai_2024_sudoku_extreme_v2,
  title        = {Hardest Sudoku Puzzle Dataset V2},
  author       = {{Sapient AI}},
  year         = {2024},
  howpublished = {\url{https://huggingface.co/datasets/sapientinc/sudoku-extreme}},
  note         = {Accessed: 2025-08-13}
}
```

### Paper: Hierarchical Reasoning Model (HRM)

If you use results or ideas from HRM, please cite their paper:

```bibtex
@misc{wang2025hierarchicalreasoningmodel,
  title         = {Hierarchical Reasoning Model},
  author        = {Guan Wang and Jin Li and Yuhao Sun and Xing Chen and Changling Liu and Yue Wu and Meng Lu and Sen Song and Yasin Abbasi Yadkori},
  year          = {2025},
  eprint        = {2506.21734},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  url           = {https://arxiv.org/abs/2506.21734}
}
```

---

## License

**Your code:** MIT License.

* This repository’s **source code** is licensed under MIT. A full LICENSE text is included below for copy‑paste. Add `SPDX-License-Identifier: MIT` to new source files.
* Third‑party assets (datasets, papers, and external repos) keep **their own licenses/terms**. See **Third‑Party Notices** and **Data usage** below.

### Third‑Party Notices (summary)

* **HRM (sapientinc/HRM)** — *Apache‑2.0*. We **do not bundle HRM code** here. If you later import/copy HRM code or ship binaries containing it, include a copy of the Apache‑2.0 license and preserve any `NOTICE` provided by HRM. Attribute the authors and indicate significant changes.
* **tdoku (t-dillon/tdoku)** — *BSD‑2‑Clause*. We do **not** ship tdoku code; the dataset’s “rating” uses tdoku for backtrack counts. If you embed tdoku, retain its copyright notice and license text in source/binaries.
* **Dataset: sapientinc/sudoku‑extreme** — License not explicitly stated in the dataset card at the time of writing. We **do not redistribute** the CSVs; instead, we provide a script that downloads them from Hugging Face. Follow the dataset card’s Usage Guidelines and any terms shown there.

### Data usage

* This repo provides **download scripts only** for `sapientinc/sudoku‑extreme` and stores derived **.npy** groupings locally. Please consult the dataset card for terms and avoid rehosting the raw CSVs in this repo or in your releases.

---

## Copy‑paste LICENSE & Notices

### `LICENSE` (MIT)

```text
MIT License

Copyright (c) 2025 VUCA INC.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### `THIRD_PARTY_NOTICES.md`

```markdown
# Third‑Party Notices

This project may refer to or integrate the following third‑party materials. Each item retains its own license/terms.

## HRM — Hierarchical Reasoning Model
- Upstream: https://github.com/sapientinc/HRM
- License: Apache‑2.0
- Notes: We do not bundle HRM code. If you import or ship HRM code, include the Apache‑2.0 LICENSE and preserve any NOTICE from upstream; attribute authors and indicate significant changes.

## Tdoku — Fast Sudoku Solver
- Upstream: https://github.com/t-dillon/tdoku
- License: BSD‑2‑Clause
- Notes: We do not bundle tdoku code. If you embed it, retain its copyright notice and license text in source and/or distribution.

## Dataset — sapientinc/sudoku‑extreme (Hardest Sudoku Puzzle Dataset V2)
- Upstream: https://huggingface.co/datasets/sapientinc/sudoku-extreme
- License: not explicitly stated in the dataset card at the time of writing
- Notes: This repo does not redistribute the dataset. Use the provided script to download from Hugging Face and follow the dataset card’s Usage Guidelines.
```

---

## Acknowledgements

* **Dataset**: Sapient AI’s *Hardest Sudoku Puzzle Dataset V2* on Hugging Face (`sapientinc/sudoku-extreme`).

* **Upstream sources referenced by the dataset**: `tdoku` benchmarks and the `enjoysudoku` community.

* **Dataset**: Sapient AI’s *Hardest Sudoku Puzzle Dataset V2* on Hugging Face (`sapientinc/sudoku-extreme`).

* **Upstream sources referenced by the dataset**: `tdoku` benchmarks and the `enjoysudoku` community.
