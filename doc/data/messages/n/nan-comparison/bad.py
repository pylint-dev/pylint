import math

import numpy as np


def both_unknown(apple, banana) -> bool:
    # Nothing equals NaN, not even NaN itself, so this is always False
    return apple == math.nan and banana == np.nan  # [nan-comparison, nan-comparison]
