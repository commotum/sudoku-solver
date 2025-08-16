"""Run a random puzzle from a specific level."""

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
from engine.utils import data_dir, is_valid_level


def _load_level(level: int) -> tuple[np.ndarray, np.ndarray]:
    """Load input and output arrays for the given level."""
    base = data_dir()
    inputs = np.load(base / f"lvl-{level}-inputs.npy")
    outputs = np.load(base / f"lvl-{level}-outputs.npy")
    return inputs, outputs


def run(level: int) -> int:
    """Solve and display a random puzzle from ``level``."""
    assert is_valid_level(level), f"invalid level: {level}"
    inputs, outputs = _load_level(level)
    num_puzzles = inputs.shape[0]
    idx = random.randint(0, num_puzzles - 1)

    selected_input = inputs[idx : idx + 1]
    selected_output = outputs[idx : idx + 1]

    print_program_header()
    print_puzzle_selection(level, num_puzzles, idx)
    print_initial_grid(selected_input[0])
    sequences, solved_flags = solve_batch(selected_input, selected_output)
    print_step_header()
    final_grid, steps, total_placements = display_sequence(
        selected_input[0], sequences[0]
    )
    print_final_output(final_grid, steps, total_placements, solved_flags[0])
    return 0
