import numpy as np


def init_lattice(grid: np.ndarray) -> np.ndarray:
    """Create candidate lattice for a single Sudoku grid.

    Parameters
    ----------
    grid : np.ndarray
        9x9 array with 0 for empty cells and 1-9 for fixed values.

    Returns
    -------
    np.ndarray
        Boolean array of shape (9, 9, 9) where lattice[r, c, k] is True if
        value ``k+1`` is currently a candidate for cell ``(r, c)``.
    """
    if grid.shape != (9, 9):
        raise ValueError("grid must be 9x9")

    lattice = np.ones((9, 9, 9), dtype=bool)

    for r in range(9):
        for c in range(9):
            v = grid[r, c]
            if v == 0:
                continue
            lattice[r, c, :] = False
            lattice[r, c, v - 1] = True
            lattice[r, :, v - 1] = False
            lattice[:, c, v - 1] = False
            br, bc = (r // 3) * 3, (c // 3) * 3
            lattice[br:br + 3, bc:bc + 3, v - 1] = False
            lattice[r, c, v - 1] = True
    return lattice


def fill_cell(grid: np.ndarray, lattice: np.ndarray, r: int, c: int, v: int) -> None:
    """Fill a cell with value ``v`` and update lattice in-place."""
    grid[r, c] = v
    lattice[r, c, :] = False
    lattice[r, c, v - 1] = True
    lattice[r, :, v - 1] = False
    lattice[:, c, v - 1] = False
    br, bc = (r // 3) * 3, (c // 3) * 3
    lattice[br:br + 3, bc:bc + 3, v - 1] = False
    lattice[r, c, v - 1] = True


def eliminate(lattice: np.ndarray, positions: list[tuple[int, int]], v: int) -> int:
    """Eliminate candidate ``v`` from given positions.

    Returns number of eliminations actually applied."""
    count = 0
    for r, c in positions:
        if lattice[r, c, v - 1]:
            lattice[r, c, v - 1] = False
            count += 1
    return count


def lattice_cell_values(lattice: np.ndarray, r: int, c: int) -> list[int]:
    """Return candidate values available for cell (r, c)."""
    return list(np.where(lattice[r, c])[0] + 1)
