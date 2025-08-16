I've been working with a dataset creator that creates vectorized numpy arrays representing various puzzles and it flattens everything into a sequence at the end for fast processing. I've invented a new type of positional encoding called MonSTERs (Minkowski Space-Time Embedding Rotors) that allows transformers to see more than just temporal sequences. Along with that I've come up with the following next step for my implementation plan:

Step 1: Extend dataset metadata for coordinate support
Key Files & Modules: dataset/common.py, dataset/*_dataset.py

Conceptual Changes Required:

Add fields to PuzzleDatasetMetadata describing coordinate dimensionality (e.g., coord_dims or per‑axis sizes).

Modify builders (build_sudoku_dataset.py, build_arc_dataset.py, etc.) so every example outputs a positions array of shape (seq_len, coord_dims) representing the coordinate of each token. Save these arrays in .npy alongside existing inputs/labels.

Dependencies & Rationale:

Metadata must describe coordinate shapes before the loader or model can use them.

Builders must emit coordinates so the loader and positional encoders have explicit spatial information.

I've attached some scripts so you can see how it works right now, but the one thing I think I need to figure out is this:

So in previous discussions we've had we've talked about the utility of using some function z = f(x,y) to augment our encoders on tasks involving 2d grids. If we don't use the z dimension at all, or the t dimension at all for that matter, we're leaving valuable parameters on the table and only encoding positional information into 1/2 of the parameters. (I think, right?) One function that's been working super well so far for the MonSTER encodings for sudoku has been z = (x % 2) + (y % 2) which gives more texture to the encodings in a symmetric double tri stripe pattern. Does this plan have any solid place for us to put our "z functions" or whether or not we'll even have one?

I mean we probably want to put that into the dataset creation part right? Like for all of the MonSTER encodings the dataset should always return a full 4d position for each token right?

But we will also have different RoPE setups too. So we need a way to parameterize these settings from the get go.

Like, for example, if we use a 9x9 sudoku puzzle, we would have different datasets for each of the following, right?

1. RoPE but using a flattened grid > sequence 1x81, [t]
2. RoPE but for a two dimensional non temporal grid 9x9 [x,y]
3. RoPE but for a two dimensional grid with solving steps Tx9x9 [t,x,y]
4. RoPE but for a three dimensional grid with time [t,x,y,z]

5. MonSTER but only using the 2d grid [0,x,y,0]
6. MonSTER but using a density function [0,x,y,z]
7. MonSTER but using a density function and temporal steps [t,x,y,z]

For the multidimensional RoPE see this excerpt from the Eleuther blog:

"### Extension to multiple dimensions

With relative ease RoPE can be extended into the multidimensional case. To represent two dimensions, two independent 1-dimensional rotary embeddings can be used. To implement this, we can split each of $\mathbf{q}$ and $\mathbf{k}$ in half and apply rotary piece-wise as follows:

$$\begin{align}
\langle f(\mathbf{q}, m, i), f(\mathbf{k}, n, j) \rangle 
&= \left\langle f_1\left(\mathbf{q}_{:d/2}, m\right), f_1\left(\mathbf{k}_{:d/2}, n\right) \right\rangle + \left\langle f_2\left(\mathbf{q}_{d/2:}, i\right), f_2\left(\mathbf{k}_{d/2:}, j\right) \right\rangle \\
&= g_1\left(\mathbf{q}_{:d/2}, \mathbf{k}_{:d/2}, m-n\right) + g_2\left(\mathbf{q}_{d/2:}, \mathbf{k}_{d/2:}, i-j\right) \\
&= g(\mathbf{q}, \mathbf{k}, m-n, i-j)
\end{align}$$

This formulation can also be further extended to data of an arbitrary number of dimensions. This sort of multi-dimensional relative coding would let us, for example, implement relative timing and relative pitch embeddings similar to Music Transformer [4] in a drastically simpler manner. More generally, we believe there is potentially a large class of invariances that first-principles positional codes like RoPE may enable us to capture."

I guess when it's all said and done I want it to work like described in this blog post:

"With the new generation of large language models, much of coding is becoming a solved problem. The real challenge now lies in systems engineering. One key lesson from years of working in distributed systems is to make your systems parametric—design them so that key variables and configurations are easy to adjust without rewriting core logic.

Each system should be organized into a file per “entity,” with clearly defined parameters or directives placed at the top for easy access. This approach makes it faster to adjust, test, and refine the system. The ultimate goal is to maximize the speed of experimentation and learning—you have to actively build and try things in order to discover what to do next."

So maybe at the very top we have some parameters:

1. Puzzle Native Dimensions (needs to denote spatial vs temporal and pair explicitly with txyz coords, so maybe an enum? For Sudoku this would clearly be t,x,y since the puzzle includes a starting board, an ending board, and rows and columns.
2. Encoder Selection (RoPE, MonSTER, Learned) Each encoder selection comes with its default dimensions and coordinate systems. 