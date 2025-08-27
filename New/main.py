

# build candidate tensor from initial grid 
    # for value in list if . then make index 0
    # if not 0 

def game_setup():
    """

    """

    # Imports initial 




def assert_value(C, G, r, c, n):
    """
    Assert a value n in cell (r, c) by updating the candidate mask C in-place.

    This function enforces the assignment of value n (0-based) to cell (r, c) in the Sudoku candidate
    mask C by:
      - Removing all other candidates from cell (r, c)
      - Removing n as a candidate value from all other cells in row r, column c, and the 3x3 box containing (r, c)
      - Setting C[r, c, n] = True to indicate n is the only candidate value for (r, c)

    Parameters
    ----------
    C : np.ndarray
        Boolean candidate mask of shape (9, 9, 9), where C[r, c, v] is True if value v (0-based) is a candidate for cell (r, c).
    r : int
        Row index of the cell (0-based).
    c : int
        Column index of the cell (0-based).
    n : int
        Value index to assign (0-based, i.e., 0 for 1, 1 for 2, ..., 8 for 9).

    Returns
    -------
    None
        The function modifies C in-place.
    """

    # Remove all candidate values from cell (r, c)
    C[r, c, :] = False

    # Remove value n as a candidate from all other cells in row r
    C[r, :, n] = False

    # Remove value n as a candidate from all other cells in column c
    C[:, c, n] = False

    # Remove value n as a candidate from all other cells in the 3x3 box containing (r, c)
    br, bc = r // 3, c // 3
    C[br*3:(br+1)*3, bc*3:(bc+1)*3, n] = False

    # Set value n as the only candidate for cell (r, c)
    C[r, c, n] = True


"""
init_background()
init_candidates_from_puzzle()

while true:
  if contradiction(): halt(NO_SOLUTION)
  if solved():       halt(SOLVED)

  fired := try_in_priority_order([
    ECP, Naked/Hidden Singles,
    Subsets (S2/S3/S4),
    Fish, Uniqueness (UR/BUG),
    Chains (Whips/Braids, typed/g-labels),
    Exotic patterns (Exocets, Tridagons, Templates), …
  ])

  if not fired:
    if T&E/DFS enabled: branch with new context and continue
    else halt(STUCK)

## The Four Elementary Constraint Propagation Rules

If a value is asserted for a cell:

1. **ECP Cell**: Eliminate all other candidates from that cell.
2. **ECP Row**: Eliminate the asserted value as a candidate from each of the row's remaining cells.
3. **ECP Column**: Eliminate the asserted value as a candidate from each of the column's remaining cells.
4. **ECP Block**: Eliminate the asserted value as a candidate from each of the block's remaining cells.

# Nine by Nine

Nine-by-Nine is a NumPy-accelerated Sudoku engine built to generate explainable, human-like reasoning traces and full step-by-step resolution paths for spatiotemporal reasoning datasets. 

The Nine-by-Nine engine models each Sudoku puzzle as a Constraint Satisfaction Problem with and uses two arrays to jointly capture a complete and consistent portrait of the puzzle for every intermediate step in the resolution process.

The first is a **solution grid** `G ∈ uint8^{9×9}` where `0` denotes an empty square and `1..9` are placed numbers, and the second is a **candidate tensor** `C ∈ bool^{9×9×9}`

ECP assertions with slices (no extra structures)

When you assert (r,c)=n (Naked/Hidden Single), eliminate that digit from the row/col/block and clear the cell’s other candidates—all with slices on C:

def assert_value(C, r, c, n):        # n = 0..8 for digit 1..9
    C[r, c, :] = False               # cell: other digits out
    C[r, :, n] = False               # row: remove n elsewhere
    C[:, c, n] = False               # column: remove n elsewhere
    br, bc = r//3, c//3
    C[br*3:(br+1)*3, bc*3:(bc+1)*3, n] = False   # block: remove n elsewhere
    C[r, c, n] = True                # keep the asserted one

"""

