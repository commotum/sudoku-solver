"""Subset strategies (pairs, triples, quads) using boolean candidates."""

from itertools import combinations
import numpy as np

from engine.utils import HOUSES


def _naked_subset_in_house(mask: np.ndarray, H, out, n_idx):
    cells = np.array([mask[r, c] for r, c in H])
    for k in range(2, 5):
        for combo in combinations(range(9), k):
            subset = cells[list(combo)]
            counts = subset.sum(axis=1)
            if np.any((counts < 2) | (counts > k)):
                continue
            union = subset.any(axis=0)
            if union.sum() != k:
                continue
            elims: dict[tuple[int, int], list[int]] = {}
            for idx in range(9):
                if idx in combo:
                    continue
                overlap = cells[idx] & union
                digits = np.where(overlap)[0] + 1
                if digits.size:
                    r, c = H[idx]
                    elims.setdefault((r, c), []).extend(digits.tolist())
            if elims:
                t = {2: "naked_pair", 3: "naked_triple", 4: "naked_quad"}[k]
                out[n_idx].append({
                    "type": t,
                    "cells": [H[i] for i in combo],
                    "eliminations": list(elims.items()),
                })


def _hidden_subset_in_house(mask: np.ndarray, H, out, n_idx):
    cells = np.array([mask[r, c] for r, c in H])
    for k in range(2, 5):
        for digits in combinations(range(9), k):
            digit_mask = cells[:, digits]
            positions = np.where(digit_mask.any(axis=1))[0]
            if len(positions) != k:
                continue
            elims: dict[tuple[int, int], list[int]] = {}
            for idx in positions:
                extra = [d + 1 for d in np.where(cells[idx])[0] if d not in digits]
                if extra:
                    r, c = H[idx]
                    elims[(r, c)] = extra
            if elims:
                t = {2: "hidden_pair", 3: "hidden_triple", 4: "hidden_quad"}[k]
                out[n_idx].append({
                    "type": t,
                    "cells": [H[i] for i in positions],
                    "eliminations": list(elims.items()),
                })


def find_naked_subsets(mask: np.ndarray, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for H in HOUSES:
            _naked_subset_in_house(m, H, out, n)


def find_hidden_subsets(mask: np.ndarray, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for H in HOUSES:
            _hidden_subset_in_house(m, H, out, n)

