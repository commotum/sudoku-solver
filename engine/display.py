# Display helpers: pretty printing grids and rendering sequences

import numpy as np

from .utils import candidate_mask_init, apply_deductions


def pretty_print_grid(grid: np.ndarray, prev_grid: np.ndarray = None) -> None:
    """Pretty-print a single 9x9 Sudoku grid.

    Newly placed numbers compared to ``prev_grid`` are highlighted in red.

    Args:
        grid: The current grid to print.
        prev_grid: Optional previous grid for change highlighting.
    """

    RED = "\033[31m"
    RESET = "\033[0m"

    print("┌───────┬───────┬───────┐")
    for i in range(9):
        row_parts = []
        for block in range(3):
            block_cells = []
            for j in range(3):
                col = block * 3 + j
                cell = grid[i, col]
                val = str(cell) if cell != 0 else "."
                if (
                    prev_grid is not None
                    and grid[i, col] != prev_grid[i, col]
                    and cell != 0
                ):
                    val = RED + val + RESET
                block_cells.append(val)
            row_parts.append(" ".join(block_cells))
        print("│ " + " │ ".join(row_parts) + " │")
        if (i + 1) % 3 == 0 and i != 8:
            print("├───────┼───────┼───────┤")
    print("└───────┴───────┴───────┘")


def format_deduction(pos, val, typ) -> str:
    row = chr(ord("A") + int(pos[0]))
    col = int(pos[1]) + 1
    if typ == "naked_single":
        nice_typ = "Naked Single"
    elif typ.startswith("hidden_single_"):
        scope = typ.split("_")[-1].title()
        nice_typ = f"Hidden Single - {scope}"
    else:
        nice_typ = typ.replace("_", " ").title()
    return f"{val} at {row}{col} ({nice_typ})"


def display_sequence(initial_grid: np.ndarray, sequence: list[dict]):
    """Replay a solution sequence with pretty printing and summary statistics."""

    grid = initial_grid.copy()
    mask = candidate_mask_init(grid[np.newaxis])
    total_placements = 0
    for idx, step_info in enumerate(sequence):
        deductions = step_info["deductions"]
        prev_grid = grid.copy()
        applied = apply_deductions(grid[np.newaxis], mask, [deductions])
        total_placements += applied

        pretty_print_grid(grid, prev_grid)
        print()

        print(f"T-{step_info['step'] + 1}:  Δ +{applied}")

        unique_deds = {}
        for ded in deductions:
            if "value" in ded:
                pos = tuple(map(int, ded["position"]))
                val = int(ded["value"])
                key = (pos, val)
                if key not in unique_deds:
                    unique_deds[key] = ded["type"]

        for key, typ in unique_deds.items():
            pos, val = key
            print(format_deduction(pos, val, typ))

        print()
        if idx != len(sequence) - 1:
            print("------------------------------------")
            print()

    return grid, len(sequence), total_placements


# ---- Main program section helpers ----


def print_program_header() -> None:
    """Print the program's banner."""

    print()
    print("====================================")
    print("Sudoku Solver v1.0")
    print("====================================")
    print()


def print_puzzle_selection(level: int, num_puzzles: int, idx: int) -> None:
    """Print information about the randomly selected puzzle."""

    print("Puzzle Chosen:")
    print(f"- Difficulty Level: {level}")
    print(f"- Puzzles @ Level : {num_puzzles-1}")
    print(f"- Selected Puzzle : {idx}")
    print()


def print_initial_grid(grid: np.ndarray) -> None:
    """Print the initial puzzle grid."""

    print("Initial Puzzle Grid:")
    pretty_print_grid(grid)
    print()


def print_step_header() -> None:
    """Print the header before the step-by-step solution."""

    print("====================================")
    print("Step by Step Solution:")
    print("====================================")
    print()


def print_final_output(
    final_grid: np.ndarray, steps: int, total_placements: int, solved: bool
) -> None:
    """Print the final grid and summary information.

    Args:
        final_grid: The resulting grid after applying deductions.
        steps: Number of steps taken.
        total_placements: Total placements applied.
        solved: Whether the puzzle was solved.
    """

    print("====================================")
    print("Final Grid:")
    print("====================================")
    print()
    pretty_print_grid(final_grid)
    print()
    if solved:
        print("Puzzle Solved!")
    else:
        print("Puzzle Unsolved.")
    print(f"- Total Steps: {steps}")
    print(f"- Total Placements: {total_placements}")
    print()
    print("====================================")
    print("PROGRAM END.")
    print("====================================")
    print()

