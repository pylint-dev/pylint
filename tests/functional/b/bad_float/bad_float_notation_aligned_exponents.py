# pylint: disable=missing-docstring,invalid-name

# A measurement and its margin of error are written on one exponent so the
# reader can see the relative precision at a glance. The odd mantissa is the
# whole point, so neither literal is flagged.
boltzmann = ("k_B", 1.3806488e-23, 0.0000013e-23)
planck = ("h", 6.62606957e-34, 0.00000029e-34)

# The statement spans several physical lines, and the pair still sees itself.
gravitation = (
    "G",
    6.67384e-11,
    0.00080e-11,
)

# Alone on its statement, with nothing to line up against.
lonely_uncertainty = 0.0000013e-23  # [bad-float-notation]

# Two exponents that merely sit near each other, without matching.
mismatched_low = 0.00012e-3  # [bad-float-notation]
mismatched_high = 0.00012e-6  # [bad-float-notation]
