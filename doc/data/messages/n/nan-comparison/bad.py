import numpy as np


def both_nan(x, y) -> bool:
    return x == np.NaN and y == float("nan")  # [nan-comparison, nan-comparison]
