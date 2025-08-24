"""Analyze all puzzle levels and generate a comprehensive report."""

from __future__ import annotations

import numpy as np
from pathlib import Path

from engine.utils import data_dir, is_valid_level


def _load_level(level: int) -> tuple[np.ndarray, np.ndarray]:
    """Load input and output arrays for the given level."""
    base = data_dir()
    inputs = np.load(base / f"lvl-{level}-inputs.npy")
    outputs = np.load(base / f"lvl-{level}-outputs.npy")
    return inputs, outputs


def _get_all_levels() -> list[int]:
    """Get all available level numbers from the data directory."""
    base = data_dir()
    level_files = [f for f in base.glob("lvl-*-inputs.npy")]
    levels = []
    
    for file_path in level_files:
        # Extract level number from filename like "lvl-42-inputs.npy"
        filename = file_path.stem  # "lvl-42-inputs"
        level_str = filename.split("-")[1]  # "42"
        try:
            level = int(level_str)
            levels.append(level)
        except ValueError:
            continue
    
    return sorted(levels)


def run() -> int:
    """Analyze all puzzle levels and generate a comprehensive report."""
    print("Analyzing all puzzle levels...")
    print("=" * 50)
    
    # Get all available levels
    all_levels = _get_all_levels()
    level_stats = {}
    
    # Process each level
    for level in all_levels:
        try:
            inputs, outputs = _load_level(level)
            num_puzzles = inputs.shape[0]
            level_stats[level] = num_puzzles
            print(f"Puzzles @ Level {level}: {num_puzzles}")
        except Exception as e:
            print(f"Error loading level {level}: {e}")
            continue
    
    # Calculate total puzzles
    total_puzzles = sum(level_stats.values())
    print(f"\nTotal Puzzles: {total_puzzles}")
    
    # Calculate percentages and prepare table
    print("\n" + "=" * 50)
    print("| Level | Puzzles | Percent |")
    print("|-------|---------|---------|")
    
    for level in sorted(level_stats.keys()):
        num_puzzles = level_stats[level]
        percentage = (num_puzzles / total_puzzles) * 100
        print(f"| {level:5d} | {num_puzzles:7d} | {percentage:6.1f}% |")
    
    print("=" * 50)
    
    return 0


if __name__ == "__main__":
    run()