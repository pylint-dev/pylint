# pylint: disable=missing-docstring,invalid-name

# Allowed: engineering OR underscore. Scientific exponent form is rejected.

# engineering — accepted
eng = 12.345e9
eng_round = 1.0e6  # base 1.0, exp 6 (multiple of 3) — engineering OK

# underscore form — accepted
under = 1_000_000.0
under_grouped = 12_345_678_900.0

# scientific-only form (base in [1, 10), exponent NOT multiple of 3) — flagged
sci_form = 1.5e10  # [bad-number-notation]
sci_form_2 = 4.5e7  # [bad-number-notation]

# Bad underscore grouping — still flagged
bad_grouping = 1_23_456_789.0  # [bad-number-notation]

# Plain literal above threshold — flagged
above_threshold = 10000000.0  # [bad-number-notation]
