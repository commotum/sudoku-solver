# SPDX-License-Identifier: MIT
"""Print list and command for a random puzzle from a given level."""

from __future__ import annotations

import random
from pathlib import Path
import sys
import numpy as np

if __package__ is None:  # allow running as a script
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from engine.utils import data_dir, is_valid_level


def _load_level(level: int) -> np.ndarray:
    """Load input array for the given level."""
    base = data_dir()
    return np.load(base / f"lvl-{level}-inputs.npy")


def run(level: int) -> int:
    """Pick a random puzzle from ``level`` and print it."""
    assert is_valid_level(level), f"invalid level: {level}"
    inputs = _load_level(level)
    num_puzzles = inputs.shape[0]
    idx = random.randint(0, num_puzzles - 1)
    puzzle = inputs[idx]
    puzzle_list = puzzle.flatten().tolist()
    puzzle_str = "".join(str(n) if n else "." for n in puzzle_list)
    print(puzzle_list)
    print(f'(solve "{puzzle_str}")')
    return 0


if __name__ == "__main__":  # pragma: no cover - convenience CLI
    import sys

    if len(sys.argv) != 2:
        print("Usage: list_puzzle.py LEVEL")
        raise SystemExit(1)
    raise SystemExit(run(int(sys.argv[1])))
