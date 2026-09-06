# pylint: disable=missing-docstring,invalid-name

exponent_not_multiple_of_three = 123e4  # [bad-float-notation]
base_not_between_one_and_a_thousand = 12345e6  # [bad-float-notation]
above_threshold_without_exponent = 10000000.0  # [bad-float-notation]
under_a_thousand_with_exponent = 9.9e2  # [bad-float-notation]
exponent_multiple_of_three = 1.23e6
base_between_one_and_a_thousand = 12.345e9
under_a_thousand = 990.0
