# pylint: disable=missing-docstring,invalid-name

# Content of bad/good.py
mindless_anarchy = 1504e5  # [bad-float-notation]
scientific_notation = 1.504e8
engineering_notation = 150.4e6
underscore_notation = 150_400_000

# Content of pep515 strict tests tested with default configuration
not_grouped_by_three = 1_23_456_7_89  # [bad-float-notation]
mixing_with_exponent = 1_23_4_5_67_8e9  # [bad-float-notation]
above_threshold_without_grouping = 123456789  # [bad-float-notation]
proper_grouping = 123_456_789
scientific_notation_2 = 1.2345678e16
engineering_notation_2 = 12.345678e15

# Content of bad_float_engineering_notation.py strict tests tested with default configuration
exponent_not_multiple_of_three = 123e4  # [bad-float-notation]
base_not_between_one_and_a_thousand = 12345e6  # [bad-float-notation]
above_threshold_without_exponent = 10000000  # [bad-float-notation]
under_a_thousand_with_exponent = 9.9e2  # [bad-float-notation]
exponent_multiple_of_three = 1.23e6
base_between_one_and_a_thousand = 12.345e9
under_a_thousand = 990

# Content of bad_float_scientific_notation strict tests tested with default configuration
base_not_between_one_and_ten = 10e3
above_threshold_without_exponent_2 = 10000000  # [bad-float-notation]
under_ten_with_exponent = 9.9e0  # [bad-float-notation]
base_between_one_and_ten = 1e4
above_threshold_with_exponent = 1e7
under_ten = 9.9


wrong_big = 45.3e7  # [bad-float-notation]
uppercase_e_wrong = 45.3E7  # [bad-float-notation]
wrong_small = 0.00012e-26  # [bad-float-notation]
uppercase_e_wrong_small = 0.00012E-26  # [bad-float-notation]
wrong_negative_and_big = -10e5  # [bad-float-notation]
actual_trolling = 11000e27  # [bad-float-notation]
scientific_double_digit = 12e8  # [bad-float-notation]
scientific_triple_digit = 123e3
zero_before_decimal_small = 0.0001e-5  # [bad-float-notation]
zero_before_decimal_big = 0.0001e5  # [bad-float-notation]
negative_decimal = -0.5e10  # [bad-float-notation]
zero_only = 0e10  # [bad-float-notation]

one_only = 1e6
correct_1 = 4.53e7
uppercase_e_correct = 4.53E7
uppercase_e_with_plus = 1.2E+10
uppercase_e_with_minus = 5.67E-8
correct_2 = 1.2e-28
correct_3 = -1.0e4
correct_4 = 1.1E30
correct_with_digits = 4.567e8
correct_with_plus = 1.2e+10
correct_decimal_only = 3.14
negative_correct = -5.67e-8
correct_small_exponent = 1.5e1  # [bad-float-notation]
actually_nine = 9e0  # [bad-float-notation]
actually_one = 1.0e0  # [bad-float-notation]

hex_constant = 0x1e4  # Hexadecimal, not scientific notation
hex_constant_bad = 0x10e4
binary_constant = 0b1010
octal_constant = 0o1234
inside_string = "Temperature: 10e3 degrees"
inside_multiline = """
This is a test with 45.3e6 inside
"""
inside_comment = 1.0  # This comment has 12e4 in it
in_variable_name = measurement_10e3 = 45
inside_f_string = f"Value is {1.0} not 10e6"

complex_number = 1.5e3 + 2.5e3j  # Complex number with scientific notation
# false negative for complex numbers:
complex_number_wrong = 15e4 + 25e7j  # [bad-float-notation]
underscore_binary = 0b1010_1010


#+1: [bad-float-notation, bad-float-notation]
def function_with_sci(param=10.0e4, other_param=20.0e5):
    return param, other_param

#+1: [bad-float-notation, bad-float-notation]
result = function_with_sci(20.0e4, 10.0e7)

valid_underscore_int = 1_000_000
valid_underscore_float = 1_000_000.12345
valid_underscore_float_exp = 123_000_000.12345e12_000_000 # [bad-float-notation]
valid_underscore_float_exp_cap = 123_000_000.12345E123_000_000 # [bad-float-notation]

invalid_underscore_octal = 0o123_456 # octal with underscores bypassed
invalid_underscore_hexa = 0x12c_456 # hexa with underscores bypassed

invalid_underscore_float_no_int = .123_456 # [bad-float-notation]
invalid_underscore_float_no_frac = 123_456.123_456 # [bad-float-notation]
incorrect_sci_underscore = 1.234_567e6 # [bad-float-notation]
incorrect_sci_uppercase = 1.234_567E6 # [bad-float-notation]
incorrect_sci_underscore_exp = 1.2e1_0  # [bad-float-notation]
invalid_underscore_float = 1_234.567_89 # [bad-float-notation]
wrong_big_underscore = 45.3_45e6 # [bad-float-notation]
wrong_small_underscore = 0.000_12e-26  # [bad-float-notation]
scientific_double_digit_underscore = 1_2e8   # [bad-float-notation]
scientific_triple_digit_underscore = 12_3e3  # [bad-float-notation]
invalid_underscore_sci = 1_234.567_89e10  # [bad-float-notation]
invalid_underscore_sci_exp = 1.2e1_0 # [bad-float-notation]
invalid_underscore_sci_combined = 1_2.3_4e5_6 # [bad-float-notation]
invalid_uppercase_sci = 1_234.567_89E10 # [bad-float-notation]
edge_underscore_1 = 1_0e6  # [bad-float-notation]
mixed_underscore_1 = 1_000_000.0e-3  # [bad-float-notation]
mixed_underscore_2 = 0.000_001e3 # [bad-float-notation]
mixed_underscore_3 = 1_0.0e2 # [bad-float-notation]

# Complex numbers with underscores
complex_underscore = 1.5_6e3 + 2.5_6e3j # [bad-float-notation]
complex_underscore_wrong = 15_6e2 + 25_6e2j # [bad-float-notation]

#+1: [bad-float-notation, bad-float-notation]
def function_with_underscore(param=10.0_0e3, other_param=20.0_0e3):
    return param, other_param

int_under_ten = 9
int_under_a_thousand = 998

for i in range(10):
    if i < 0:
        continue
    print("Let's not be really annoying.")
