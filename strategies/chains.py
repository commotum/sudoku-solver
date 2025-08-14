import numpy as np
from collections import deque, defaultdict


PEERS = {}
for r in range(9):
    for c in range(9):
        peers = {(r, j) for j in range(9) if j != c}
        peers |= {(i, c) for i in range(9) if i != r}
        br, bc = (r // 3) * 3, (c // 3) * 3
        peers |= {(br + i, bc + j) for i in range(3) for j in range(3)}
        peers.remove((r, c))
        PEERS[(r, c)] = peers


def simple_coloring(lattice: np.ndarray, grid: np.ndarray) -> list[dict]:
    """Apply simple coloring on each digit."""
    deductions: list[dict] = []
    for k in range(9):
        # Build graph of strong links
        graph = defaultdict(set)
        # Rows
        for r in range(9):
            cells = np.where(lattice[r, :, k])[0]
            if len(cells) == 2:
                a, b = cells
                graph[(r, int(a))].add((r, int(b)))
                graph[(r, int(b))].add((r, int(a)))
        # Columns
        for c in range(9):
            cells = np.where(lattice[:, c, k])[0]
            if len(cells) == 2:
                a, b = cells
                graph[(int(a), c)].add((int(b), c))
                graph[(int(b), c)].add((int(a), c))
        # Boxes
        for br in range(3):
            for bc in range(3):
                sub = lattice[br*3:(br+1)*3, bc*3:(bc+1)*3, k]
                cells = np.argwhere(sub)
                if len(cells) == 2:
                    (r1, c1), (r2, c2) = cells
                    cell1 = (br*3 + int(r1), bc*3 + int(c1))
                    cell2 = (br*3 + int(r2), bc*3 + int(c2))
                    graph[cell1].add(cell2)
                    graph[cell2].add(cell1)
        colored = {}
        for node in graph:
            if node in colored:
                continue
            queue = deque([(node, 0)])
            colored[node] = 0
            groups = {0: {node}, 1: set()}
            while queue:
                cell, color = queue.popleft()
                for neigh in graph[cell]:
                    if neigh not in colored:
                        colored[neigh] = 1 - color
                        groups[1 - color].add(neigh)
                        queue.append((neigh, 1 - color))
            # Check for contradictions
            for color, cells in groups.items():
                # any unit with two same color? -> eliminate this color group
                conflict = False
                rows = defaultdict(list)
                cols = defaultdict(list)
                boxes = defaultdict(list)
                for r, c in cells:
                    rows[r].append((r, c))
                    cols[c].append((r, c))
                    boxes[(r//3, c//3)].append((r, c))
                if any(len(v) > 1 for v in rows.values()) or any(len(v) > 1 for v in cols.values()) or any(len(v) > 1 for v in boxes.values()):
                    conflict = True
                if conflict:
                    elims = []
                    for r, c in cells:
                        if lattice[r, c, k]:
                            elims.append(((r, c), [k + 1]))
                    if elims:
                        deductions.append({'type': 'simple_coloring',
                                           'value': k + 1,
                                           'eliminations': elims})
    return deductions
