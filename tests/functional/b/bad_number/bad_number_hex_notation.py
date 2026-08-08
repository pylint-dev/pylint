# pylint: disable=missing-docstring,invalid-name

# Bad: underscores in wrong positions
wrong_grouping_1 = 0x12c_456  # [bad-number-notation]
wrong_grouping_2 = 0xDE_AD_BE_EF  # [bad-number-notation]
wrong_grouping_3 = 0x123_4567_89  # [bad-number-notation]
wrong_grouping_4 = 0xABCDE_F  # [bad-number-notation]
wrong_grouping_5 = 0xA_B  # [bad-number-notation]

# Not flagged by default: above threshold but suggest-int-underscore is off
big_hex_no_grouping = 0xDEADBEEF
big_hex_no_grouping_2 = 0x1234567890ABCDEF
big_hex_no_grouping_3 = 0xF4240

# Good: properly grouped by 4
proper_grouping_1 = 0xDEAD_BEEF
proper_grouping_2 = 0x1234_5678_90AB_CDEF
proper_grouping_3 = 0x1_0000
proper_grouping_4 = 0xAB_CDEF
proper_grouping_5 = 0x1_2345_6789

# Good: small hex (below threshold), no grouping needed
small_hex_1 = 0xFF
small_hex_2 = 0x1A2B
small_hex_3 = 0x0
small_hex_4 = 0xF423F

# Good: uppercase X prefix, properly grouped
upper_prefix = 0XDEAD_BEEF
