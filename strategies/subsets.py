from itertools import combinations
import numpy as np

from engine.utils import HOUSES, digits_from_mask, ALL_CANDIDATES


def _naked_subset_in_house(mask, H, out, n_idx):
    values = [mask[r, c] for r, c in H]
    for k in range(2, 5):
        for combo in combinations(range(9), k):
            union = 0
            valid = True
            for idx in combo:
                m = values[idx]
                pc = m.bit_count()
                if pc < 2 or pc > k:
                    valid = False
                    break
                union |= m
            if not valid or union.bit_count() != k:
                continue
            elims = {}
            for idx2 in range(9):
                if idx2 in combo:
                    continue
                m2 = values[idx2]
                if m2 & union:
                    r, c = H[idx2]
                    for d in digits_from_mask(m2 & union):
                        elims.setdefault((r, c), []).append(d)
            if elims:
                t = {2: "naked_pair", 3: "naked_triple", 4: "naked_quad"}[k]
                out[n_idx].append({"type": t, "cells": [H[i] for i in combo], "eliminations": list(elims.items())})

def _hidden_subset_in_house(mask, H, out, n_idx):
    values = [mask[r, c] for r, c in H]
    for k in range(2, 5):
        for digits in combinations(range(1, 10), k):
            digit_mask = 0
            for d in digits:
                digit_mask |= 1 << (d - 1)
            positions = [idx for idx in range(9) if values[idx] & digit_mask]
            if len(positions) != k:
                continue
            elims = {}
            for idx in positions:
                extra = values[idx] & (ALL_CANDIDATES & ~digit_mask)
                if extra:
                    r, c = H[idx]
                    for d in digits_from_mask(extra):
                        elims.setdefault((r, c), []).append(d)
            if elims:
                t = {2: "hidden_pair", 3: "hidden_triple", 4: "hidden_quad"}[k]
                out[n_idx].append({"type": t, "cells": [H[i] for i in positions], "eliminations": list(elims.items())})

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
