import numpy as np

from utils import digits_from_mask


def find_ur_type1(mask: np.ndarray, out: list[list[dict]]) -> None:
    N = mask.shape[0]
    for n in range(N):
        m = mask[n]
        for r1 in range(8):
            for r2 in range(r1 + 1, 9):
                for c1 in range(8):
                    for c2 in range(c1 + 1, 9):
                        cells = [
                            (r1, c1),
                            (r1, c2),
                            (r2, c1),
                            (r2, c2),
                        ]
                        masks = [m[r, c] for r, c in cells]
                        pairs = {}
                        for idx, mk in enumerate(masks):
                            if mk.bit_count() == 2:
                                pairs.setdefault(mk, []).append(idx)
                        for pair_mask, idxs in pairs.items():
                            if len(idxs) == 3:
                                x0 = ({0, 1, 2, 3} - set(idxs)).pop()
                                mk = masks[x0]
                                if mk & pair_mask == pair_mask:
                                    extra = mk & ~pair_mask
                                    if extra.bit_count() == 1:
                                        digit = digits_from_mask(extra)[0]
                                        r, c = cells[x0]
                                        out[n].append({
                                            "type": "ur_type1",
                                            "position": (r, c),
                                            "value": digit,
                                        })
