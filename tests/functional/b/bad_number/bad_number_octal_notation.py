# pylint: disable=missing-docstring,invalid-name

# Bad: underscores in wrong positions
wrong_grouping_1 = 0o12_3456  # [bad-number-notation]
wrong_grouping_2 = 0o1234_56  # [bad-number-notation]

# Bad: above threshold without underscore grouping (threshold is 1e6 = 1_000_000)
big_oct = 0o3641100  # [bad-number-notation]

# Good: properly grouped by 3
proper_grouping_1 = 0o3_641_100
proper_grouping_2 = 0o123_456
proper_grouping_3 = 0o_123_456

# Good: small octal (below threshold), no grouping needed
small_oct_1 = 0o777
small_oct_2 = 0o0
small_oct_3 = 0o777_777
