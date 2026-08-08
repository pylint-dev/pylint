# pylint: disable=missing-docstring,invalid-name

# Allowed: scientific OR underscore. Engineering exponent form is rejected.

# scientific — accepted
sci = 1.5e10
sci_2 = 4.53e7

# underscore form — accepted
under = 1_000_000.0
under_grouped = 12_345_678_900.0

# engineering-only form (base in [1, 1000), base ≥ 10) — flagged
eng_form = 12.345e9  # [bad-number-notation]
eng_form_2 = 150.4e6  # [bad-number-notation]

# Bad underscore grouping — still flagged
bad_grouping = 1_23_456_789.0  # [bad-number-notation]

# Plain literal above threshold — flagged
above_threshold = 10000000.0  # [bad-number-notation]
