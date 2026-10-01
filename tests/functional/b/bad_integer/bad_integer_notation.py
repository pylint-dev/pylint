# pylint: disable=missing-docstring,invalid-name

zero_int = 0
annoying_zero_int = 00  # [bad-integer-notation]
annoying_zero_int_2 = 000  # [bad-integer-notation]
annoying_zero_int_3 = 0_0  # [bad-integer-notation]

int_under_ten = 9
int_under_a_thousand = 998
valid_small_int = 999
under_a_thousand = 990

bad_int_grouping = 1_23_456  # [bad-integer-notation]
big_int_no_grouping = 3141592  # [bad-integer-notation]
just_under_threshold = 999999
exactly_at_threshold = 1000000  # [bad-integer-notation]
valid_grouped_int = 1_000_000
underscore_notation = 150_400_000
proper_grouping = 123_456_789

# A run of consecutive digits is recognized by its shape: grouping hides it.
ascending_run = 1234567
long_ascending_run = 123456789
keyboard_run = 1234567890
descending_run = 987654321
descending_run_to_zero = 9876543210
almost_a_run = 1234568  # [bad-integer-notation]
run_wrapping_twice = 12345678901  # [bad-integer-notation]
run_wrapping_in_the_middle = 8901234  # [bad-integer-notation]
badly_grouped_run = 1234_5678  # [bad-integer-notation]
hex_run = 0x1234567  # [bad-integer-notation]

valid_underscore_octal = 0o123_456  # correctly grouped by 3, below threshold
invalid_underscore_hexa = 0x12c_456  # [bad-integer-notation]
underscore_binary = 0b1010_1010

# A float is never this message's business, whatever its size.
large_float = 1541455200.0
