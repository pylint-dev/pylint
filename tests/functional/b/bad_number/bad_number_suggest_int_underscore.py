# pylint: disable=missing-docstring,invalid-name

# Flagged: above threshold without underscore grouping
big_int = 1234567  # [bad-number-notation]
big_hex = 0xDEADBEEF  # [bad-number-notation]
big_bin = 0b11110100001001000000  # [bad-number-notation]
big_oct = 0o3641100  # [bad-number-notation]

# Flagged: bad underscore grouping (always flagged regardless of option)
bad_grouping_int = 1_23_456  # [bad-number-notation]
bad_grouping_hex = 0xDE_AD_BE_EF  # [bad-number-notation]

# Not flagged: below threshold
small_int = 999
small_hex = 0xFF

# Not flagged: already properly grouped
valid_int = 1_000_000
valid_hex = 0xDEAD_BEEF
