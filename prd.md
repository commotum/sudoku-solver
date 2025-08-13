# Product Requirements Document (PRD): Sudoku Solver Repository

## Document Information
- **Title**: Sudoku Solver Repository - Human-Like Solving Sequence Generator
- **Version**: 1.0
- **Date**: August 12, 2025
- **Author**: @commotum
- **Status**: Draft
- **Purpose of Document**: This PRD defines the requirements, architecture, and implementation guidelines for a modular Sudoku solver repository. The solver generates extended sequences of solving steps mimicking human logic, using a dataset of puzzles to produce data suitable for training reinforcement learning neural networks. It builds on an existing dataset from Hugging Face and emphasizes modularity for easy extension.

## 1. Overview
### 1.1 Product Description
The Sudoku Solver Repository is a Python-based project designed to solve Sudoku puzzles using human-like strategies while recording each step in a sequence format. The primary goal is to transform puzzle-question-answer pairs from a dataset into detailed solving traces (e.g., grid states, deductions, and strategy applications). This enables the creation of a dataset for machine learning applications, such as training models to solve puzzles step-by-step.

Key features include:
- Downloading and processing Sudoku puzzles by difficulty level.
- A modular strategy system for applying solving techniques in a progressive order (simple to complex).
- Batched solving for efficiency on large datasets.
- Output of solving sequences in formats like .npy or JSON for further analysis or ML use.

The system prioritizes modularity to handle growing complexity, such as adding new strategies without disrupting existing code.

### 1.2 Target Audience
- Developers and researchers building ML models for puzzle-solving or logical reasoning.
- Sudoku enthusiasts or educators interested in step-by-step solving explanations.
- Open-source contributors extending Sudoku solving algorithms.

### 1.3 Business Goals
- Create a scalable tool for generating human-mimicking solving datasets.
- Promote maintainability through modular design to facilitate community contributions.
- Ensure efficiency for processing large datasets (e.g., thousands of puzzles) without performance bottlenecks.

## 2. Goals and Objectives
### 2.1 Functional Goals
- Fetch and preprocess Sudoku puzzles from a Hugging Face dataset, bucketing by difficulty.
- Implement a solver that applies strategies in a loop, recording each step until solved or stuck.
- Support batch processing for multiple puzzles to leverage vectorized operations (e.g., via NumPy).
- Generate output sequences including grid snapshots, applied deductions, and strategy metadata.
- Validate solutions against provided answers and ensure no invalid states during solving.

### 2.2 Non-Functional Goals
- **Performance**: Solve easy puzzles in <1 second, hard ones in <10 seconds; batch 1000 puzzles in <1 minute on standard hardware.
- **Modularity**: Strategies organized by type/complexity; easy to add new ones via function registration.
- **Maintainability**: Clean code structure, with tests for strategies and utilities.
- **Usability**: Command-line interface via `main.py` for easy execution; detailed README for setup and extension.
- **Scalability**: Handle puzzles up to expert difficulty; extendable to variants like larger grids if needed.

### 2.3 Success Metrics
- 100% of puzzles solved correctly (validated against dataset solutions).
- Average solving steps per difficulty level match human-like progression (e.g., <20 steps for easy puzzles).
- Code coverage >80% via tests.
- Community feedback: Easy to add a new strategy in <30 minutes.

## 3. Scope
### 3.1 In Scope
- Data downloading and processing from "sapientinc/sudoku-extreme" dataset.
- Implementation of core strategies based on the provided taxonomy (starting with singles, expandable to chains).
- Batch-enabled solver loop with step recording.
- Utility functions for grid management and validation.
- Basic CLI for running on specific difficulties/subsets.

### 3.2 Out of Scope
- GUI for visualizing solving steps (focus on CLI and data output).
- Support for non-standard Sudoku variants (e.g., 16x16 grids, irregular shapes).
- Full ML training pipeline (output data only; user handles training).
- Real-time solving or mobile app integration.
- Advanced error handling for corrupt datasets.

## 4. Requirements
### 4.1 Functional Requirements
1. **Data Processing**:
   - Download CSVs from Hugging Face, convert to 9x9 NumPy arrays.
   - Bucket puzzles by difficulty (min/max determined dynamically).
   - Save as .npy files (e.g., `lvl-<diff>-inputs.npy`, `lvl-<diff>-outputs.npy`).

2. **Strategy System**:
   - Modular functions for each strategy, operating on a candidates array (bool, shape (N,9,9,9) for batch N).
   - Central hub (`strategies.py`) to register strategies and compute deductions batched.
   - Support group strategies (e.g., `'hidden_single'` expands to row/col/box variants).

3. **Solver Loop**:
   - Initialize grids from inputs.
   - Loop: Compute candidates → Find deductions → Apply fills/eliminations → Record step → Check solved/valid.
   - Escalate strategies if no progress (e.g., start with singles, add subsets if stuck).
   - Record sequences as lists of dicts (e.g., `{'step': i, 'grid_state': grid_copy.flatten(), 'deductions': [ded_dicts]}`).

4. **Output**:
   - Save sequences per difficulty (e.g., .npy arrays or JSON).
   - Optional stats: Avg steps, strategies used, unsolved count.

5. **Utilities**:
   - Grid validation (no duplicates in rows/cols/boxes).
   - Apply deductions (fills first, then eliminations).
   - Pretty-print grids for debugging.

### 4.2 Non-Functional Requirements
- **Tech Stack**: Python 3.x, NumPy for arrays, HuggingFace Hub for data, TQDM for progress.
- **Dependencies**: Listed in `requirements.txt` (no internet-required installs during runtime).
- **Testing**: Unit tests for strategies (e.g., sample grids), integration tests for solver loop.
- **Documentation**: README with setup, run instructions, strategy taxonomy, and extension guide.

## 5. Architecture and Design
### 5.1 High-Level Architecture
The repo follows a modular, layered design:
- **Data Layer**: `dataset_download.py` handles fetching and preprocessing.
- **Strategy Layer**: Directory with per-type files; `strategies.py` as orchestrator.
- **Core Logic Layer**: `solver.py` for the solving loop and batching.
- **Utility Layer**: `utils.py` for shared helpers.
- **Entry Layer**: `main.py` for CLI orchestration.

Data flow: Data → Solver (uses Strategies + Utils) → Sequences.

### 5.2 File Structure
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

### 5.3 Workflow
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

### 5.4 Strategy Design
- Each strategy file contains functions like `find_<strategy>(candidates, all_deductions)` that append dicts to a list (e.g., `{'type': 'naked_single', 'position': (i,j), 'value': val}`).
- `strategies.py` computes candidates once (shared across strategies) and dispatches via a dictionary.
- For eliminations (e.g., in subsets), extend deduction dicts to include `'eliminations': [((i,j), [vals_to_remove])]`.

## 6. Implementation Details
### 6.1 Strategy Taxonomy
(See appendix for full table. Implementation priority: Singles first, then subsets, intersections, etc.)

- Strategies rely on a candidates array for efficiency.
- Apply in order: Singles → Subsets/Intersections → Fish/Wings → Chains.

### 6.2 Data Formats
- Grids: NumPy uint8 (9,9), 0 for empty.
- Sequences: List of dicts per puzzle, serialized to .npy or JSON.

### 6.3 Edge Cases
- Unsolvable puzzles: Log and skip after max iterations (e.g., 100).
- Invalid initial grids: Raise errors during loading.

## 7. Dependencies and Risks
### 7.1 Dependencies
- Python 3.10+.
- Libraries: numpy, huggingface_hub, tqdm.
- Dataset: "sapientinc/sudoku-extreme" (assume availability).

### 7.2 Risks and Mitigations
- Risk: Performance on hard puzzles → Mitigation: Escalate strategies gradually; optional timeout.
- Risk: Strategy bugs → Mitigation: Unit tests with known puzzles.
- Risk: Dataset changes → Mitigation: Version pinning in code.
- Assumptions: Users have basic Python knowledge; no GPU required.

## Appendix: Strategy Taxonomy
| Strategy              | Action Type                  | Complexity/Size      | Scope                      | Notes                                                                 |
|-----------------------|------------------------------|----------------------|----------------------------|-----------------------------------------------------------------------|
| **Naked Single**     | Certainty (fill cell)       | Single (1 candidate in cell) | Cell-only                 | Simplest: Cell has only 1 possible candidate left after basic eliminations. Applied first in most solvers. |
| **Hidden Single**    | Certainty (fill cell)       | Single (1 cell for a candidate in unit) | Unit (row/col/box)       | Candidate appears in only 1 cell in a unit; fill it. Similar to naked but "hidden" among other candidates. |
| **Locked Candidates**| Operation on unknowns (eliminate candidates) | Pair/Triple (2-3 cells in intersection) | Intersection (box-row/col) | Candidate locked to a box-line intersection; eliminate from rest of line or box. AKA Pointing (box→line) or Claiming (line→box). |
| **Naked Pair/Triplet/Quad** | Operation on unknowns (eliminate candidates) | Pair (2), Triple (3), Quad (4) cells/candidates | Unit (row/col/box)       | Group of cells in unit with exactly those candidates; eliminate them from other cells in unit. |
| **Hidden Pair/Triplet/Quad** | Operation on unknowns (eliminate candidates) | Pair (2), Triple (3), Quad (4) candidates/cells | Unit (row/col/box)       | Group of candidates appear only in those cells in unit; eliminate other candidates from those cells. Inverse of naked subsets. |
| **XY-Wing**          | Operation on unknowns (eliminate candidates) | Triple (3 cells in chain) | Chain (bivalue cells connected) | Pivot cell (XY) linked to two wings (XZ, YZ); eliminates Z where wings "see" it. Simple chain strategy. |
| **XYZ-Wing**         | Operation on unknowns (eliminate candidates) | Triple (3 cells, pivot has 3 candidates) | Chain (trivalue pivot + bivalue wings) | Extension of XY-Wing; pivot (XYZ) + wings (XZ, YZ); eliminates Z in common peer cells. |
| **X-Wing**           | Operation on unknowns (eliminate candidates) | Quad (4 cells in rectangle) | Grid-wide (2 rows + 2 cols) | Candidate in 2 rows only at 2 cols each, forming rectangle; eliminate from those cols elsewhere. Basic "fish" pattern. |
| **Swordfish**        | Operation on unknowns (eliminate candidates) | 9 cells (3x3 grid)  | Grid-wide (3 rows + 3 cols) | Like X-Wing but for 3 rows/cols; eliminates in aligned cols/rows. Advanced fish. |
| **Coloring**         | Operation on unknowns (eliminate) or certainty (if contradiction) | Variable (chain length) | Chain (candidate graph)  | Treat candidates as graph nodes, color chains; if same color sees each other, eliminate. Handles complex implications. |
| **Forcing Chain**    | Operation on unknowns (eliminate) or certainty (fill if all paths lead to same) | Variable (chain length) | Chain (implications across grid) | Follow "if A then B then C" chains; if contradiction or forced value, act. Can be short (nice loops) or long. |
| **Nishio**           | Operation on unknowns (eliminate via trial) | Variable (assumption + chain) | Trial/chain (assume candidate true/false) | Assume a candidate is true, propagate; if contradiction, eliminate it. Lightweight backtracking/trial-and-error. |

**Overall Patterns**:
- Certainty vs. Unknowns: Singles always fill (certainty). Most others eliminate (reducing unknowns), which may indirectly create new singles. Chains/trials can do both.
- Single/Double/Triple: Singles are "single," subsets scale to quad, wings/fish are fixed-size patterns (triple/quad+), chains are variable (often >3).
- Human-Like Progression: Humans start with singles (obvious fills), then subsets/intersections (local patterns), then fish/wings (grid scans), and chains/trials last (deductive reasoning). Your solver should apply in this order to generate natural sequences.
- Implementation Tip: All rely on candidates array. Simpler ones (singles/subsets) are unit-based and fast; chains are slower (graph traversal), so apply sparingly.

This taxonomy guides file grouping and solver ordering.