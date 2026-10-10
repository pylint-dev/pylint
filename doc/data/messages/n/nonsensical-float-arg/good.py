import math

BASKET = 3.0
CRATE = 12.0

if math.isclose(BASKET, CRATE, rel_tol=0.1):
    print("The basket holds about as many apples as the crate.")
