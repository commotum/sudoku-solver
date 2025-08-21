Here’s the architecture, top-down, with the “why” baked in.

Model (state):

grid\[9×9] holds placed digits (1..9, 0 for empty).

cand\[9×9×9] is a boolean tensor where cand\[r,c,n] means digit n+1 is possible at (r,c).
Why: this mirrors the set notation (C(x) ⊆ N) directly and lets us express constraints as vectorized boolean operations.

Houses & views:

Rows, columns, and 3×3 blocks are “houses.” Blocks are handled by reshaping/viewing cand into (3,3,3,3,9) and reducing on the right axes.
Why: house logic becomes axis reductions (sum/any/argmax) and masked assignments—clean, fast, NumPy-native.

Semantics (assign & propagate):

An assignment tensor A\[9×9×9] (one-hot per cell) encodes x←n. Applying A forces the chosen digit in that cell and clears it from all peers (row/col/block) via masked writes.
Why: separating “discover assignments” from “propagate effects” makes rules idempotent and composable.

Rule detectors (vectorized):

Naked single: cells where cand.sum(axis=2)==1.

Hidden single: for each house & digit, positions where the house-slice has exactly one True.

Cover (pointing/claiming): test if a digit’s Trues in an overlap are confined to one row/col; clear elsewhere by masks.

(Extend with subsets, fish, UR using small combinations on boolean slices.)
Why: each rule is a small, readable reduction + mask; results are assignments or eliminations.

Solve loop (fixpoint):

Alternate: detect → apply assignments → propagate → apply eliminations; repeat until no change.
Why: predictable convergence, easy to test, and performance comes from keeping all heavy work inside NumPy kernels.

Optional rn/cn/bn projections:

Project cand into (r,n)→cols, (c,n)→rows, (b,n)→square views for fish/uniqueness patterns.
Why: these are just rearrangements of the same tensor, matching the set-notation projections and enabling more rules without new data structures.

Goal & rationale: Make the code read like the math, showcase NumPy fluency (broadcasting, axis reductions, reshapes, masked assignment), and provide a clear, extensible baseline where adding rules is “write a reduction, apply a mask,” not “rewrite the representation.”
