import os
from typing import List, Dict, Tuple

import numpy as np

from utils import candidate_mask_init, apply_deductions
from strategies import find_deductions_batch, TIERS


def is_solved(grid: np.ndarray) -> bool:
    return np.all(grid != 0)


def solve_batch(
    inputs: np.ndarray,
    outputs: np.ndarray,
    max_steps: int = 100,
    max_tier: int = 3,
) -> Tuple[List[List[Dict]], List[bool]]:
    """Solve batch of puzzles using strategy tiers."""
    N = inputs.shape[0]
    grids = inputs.copy()
    masks = candidate_mask_init(grids)
    sequences: List[List[Dict]] = [[] for _ in range(N)]
    solved_flags = [False] * N

    for n in range(N):
        grid = grids[n]
        mask = masks[n]
        seq = sequences[n]
        step = 0
        solved = is_solved(grid)
        while not solved and step < max_steps:
            cumulative: list[str] = []
            progress = False
            for tier in range(1, max_tier + 1):
                cumulative.extend(TIERS[tier])
                prev_grid = grid.copy()
                deductions = find_deductions_batch(mask[np.newaxis], cumulative)[0]
                if not deductions:
                    continue
                apply_deductions(grid[np.newaxis], mask[np.newaxis], [deductions])
                if np.array_equal(grid, prev_grid):
                    continue
                seq.append(
                    {
                        "step": step,
                        "grid_state": prev_grid.flatten().tolist(),
                        "deductions": deductions,
                    }
                )
                progress = True
                break
            if not progress:
                solved = False
                break
            step += 1
            solved = is_solved(grid)
        solved_flags[n] = solved
    return sequences, solved_flags


def load_and_solve_difficulty(
    diff: int,
    data_dir: str = "data/sudoku-extreme-processed",
    subsample: int | None = None,
) -> Tuple[List[List[Dict]], List[bool]]:
    inputs_path = os.path.join(data_dir, f"lvl-{diff}-inputs.npy")
    outputs_path = os.path.join(data_dir, f"lvl-{diff}-outputs.npy")
    if not os.path.exists(inputs_path):
        raise FileNotFoundError(f"No data for level {diff}")
    inputs = np.load(inputs_path)
    outputs = np.load(outputs_path)
    if subsample:
        inputs = inputs[:subsample]
        outputs = outputs[:subsample]
    if diff <= 2:
        max_tier = 1
    elif diff <= 5:
        max_tier = 2
    else:
        max_tier = 3
    return solve_batch(inputs, outputs, max_tier=max_tier)
