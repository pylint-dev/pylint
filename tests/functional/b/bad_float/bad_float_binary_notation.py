# pylint: disable=missing-docstring,invalid-name

# Bad: underscores in wrong positions
wrong_grouping_1 = 0b1111_001  # [bad-float-notation]
wrong_grouping_2 = 0b11111_0011  # [bad-float-notation]
wrong_grouping_3 = 0b1_11_0011  # [bad-float-notation]

# Bad: above threshold without underscore grouping (threshold is 1e6 = 1_000_000)
big_bin = 0b11110100001001000000  # [bad-float-notation]

# Good: properly grouped by 4
proper_grouping_1 = 0b0011_1111_0100_1110
proper_grouping_2 = 0b_0011_1111
proper_grouping_3 = 0b1_0000
proper_grouping_4 = 0b11_0011

# Good: small binary (below threshold), no grouping needed
small_bin_1 = 0b1010
small_bin_2 = 0b1
small_bin_3 = 0b0
small_bin_4 = 0b1111_1111_1111_1111
