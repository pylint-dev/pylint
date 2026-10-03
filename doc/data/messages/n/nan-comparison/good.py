import math

import numpy as np


def both_unknown(apple, banana) -> bool:
    return math.isnan(apple) and np.isnan(banana)
