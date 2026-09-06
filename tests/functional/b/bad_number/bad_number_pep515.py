# pylint: disable=missing-docstring,invalid-name

not_grouped_by_three = 1_23_456_7_89.0  # [bad-number-notation]
mixing_with_exponent = 1_23_4_5_67_8e9  # [bad-number-notation]
above_threshold_without_grouping = 123456789.0  # [bad-number-notation]
scientific_notation = 1.2345678e16 # [bad-number-notation]
engineering_notation = 12.345678e15 # [bad-number-notation]

proper_grouping = 123_456_789.0

int_under_ten = 9
