# pylint: disable=missing-docstring,invalid-name

# A rewrite that pays for itself.
round_value = 100000000.0  # [bad-float-notation]

# These get no shorter once rewritten, so at a min-gain of 1 they are left
# alone rather than churned.
speed_of_light = 299792458.0
long_mantissa = 5724535.74068625
julian_date = 2456165.5

# A literal that already picked a notation and got it wrong is flagged
# whatever the gain: that is a mistake, not a matter of taste.
base_too_big = 12345e6  # [bad-float-notation]
bad_grouping = 1_23_456_7_89.0  # [bad-float-notation]
