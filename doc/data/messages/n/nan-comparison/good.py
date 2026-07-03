import numpy as np


def both_nan(x, y) -> bool:
    return np.isnan(x) and np.isnan(y)
