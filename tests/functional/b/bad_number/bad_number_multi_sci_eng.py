# pylint: disable=missing-docstring,invalid-name

# Allowed: scientific OR engineering form. Underscore is rejected.

# scientific (base in [1, 10)) — accepted
sci = 1.5e10

# engineering (base in [1, 1000), exponent multiple of 3) — accepted
eng = 12.345e9

# scientific OK even when engineering form is wrong (exponent not multiple of 3)
sci_only_match = 1.5e10  # 10 % 3 != 0 but base in [1, 10)

# engineering OK even when scientific form is wrong (base ≥ 10)
eng_only_match = 12.345e9  # base 12.345 not in [1, 10)

# Neither form matches: base too big AND exponent not multiple of 3
neither = 12345e7  # [bad-number-notation]

# Underscore literal — rejected because underscore is not allowed
no_underscore = 10_000_000.0  # [bad-number-notation]
no_underscore_grouping = 1_000_000_000.5  # [bad-number-notation]

# Plain literal above threshold without an exponent — flagged like in default mode
above_threshold = 10000000.0  # [bad-number-notation]
