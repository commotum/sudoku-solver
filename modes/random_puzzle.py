"""Random puzzle mode."""

from __future__ import annotations

import random

import numpy as np

from engine.solver import solve_batch
from engine.display import (
    print_program_header,
    print_puzzle_selection,
    print_initial_grid,
    print_step_header,
    display_sequence,
    print_final_output,
)
from engine.utils import data_dir, is_valid_level, random_level


def _load_level(level: int) -> tuple[np.ndarray, np.ndarray]:
    """Load arrays for ``level``."""
    base = data_dir()
    inputs = np.load(base / f"lvl-{level}-inputs.npy")
    outputs = np.load(base / f"lvl-{level}-outputs.npy")
    return inputs, outputs


def run(level: int | None = None) -> int:
    """Solve a random puzzle.

    If ``level`` is ``None`` choose uniformly from all available levels,
    otherwise choose a random puzzle from the specified level.
    """
    lvl = level if (level is not None and is_valid_level(level)) else None
    if lvl is None:
        lvl = random_level()
    inputs, outputs = _load_level(lvl)
    num_puzzles = inputs.shape[0]
    idx = random.randint(0, num_puzzles - 1)

    selected_input = inputs[idx : idx + 1]
    selected_output = outputs[idx : idx + 1]

    print_program_header()
    print_puzzle_selection(lvl, num_puzzles, idx)
    print_initial_grid(selected_input[0])
    sequences, solved_flags = solve_batch(selected_input, selected_output)
    print_step_header()
    final_grid, steps, total_placements = display_sequence(
        selected_input[0], sequences[0]
    )
    print_final_output(final_grid, steps, total_placements, solved_flags[0])
    return 0
