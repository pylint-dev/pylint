# pylint: disable=missing-docstring,invalid-name

# Float overflow — evaluates to math.inf at runtime
huge_number = 1.5e500  # [bad-float-precision]
just_overflowing = 1.5e309  # [bad-float-precision]
# Largest representable double — not flagged
near_max = 1.5e308

# Float underflow — evaluates to 0.0 at runtime
tiny_number = 1e-1000  # [bad-float-precision]
tiny_number_2 = 1.5e-500  # [bad-float-precision]
# Subnormal but representable — not flagged
subnormal = 5e-324

# More than 15 significant digits — float can't represent exactly
pi_22_digits = 3.14159265358979323846  # [bad-float-precision]

# Boundary: exactly 15 sig figs, no precision loss
fifteen_digits = 1.23456789012345
