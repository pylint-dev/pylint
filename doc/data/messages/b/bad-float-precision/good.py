import decimal
import math

# Pick the runtime-equivalent literal if you wanted that value:
huge_number_inf = math.inf
tiny_number_zero = 0.0
pi_float = 3.141592653589793  # same thing than with giving more digit as a float

# Or pick decimal.Decimal if you need to preserve the source precision
# (the value won't go through float at all):
huge_number_precise = decimal.Decimal("1.5e500")
tiny_number_precise = decimal.Decimal("1e-1000")
pi_precise = decimal.Decimal("3.14159265358979323846")
