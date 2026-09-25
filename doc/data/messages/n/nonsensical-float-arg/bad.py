import math

BASKET = 3.0
CRATE = 12.0

if math.isclose(BASKET, CRATE, rel_tol=math.inf):  # [nonsensical-float-arg]
    print("The basket holds about as many apples as the crate.")
