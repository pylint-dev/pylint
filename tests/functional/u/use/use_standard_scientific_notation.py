# pylint: disable=missing-docstring,invalid-name

wrong_big = 45.3e6  # [use-standard-scientific-notation]
uppercase_e_wrong = 45.3E6  # [use-standard-scientific-notation]
wrong_small = 0.00012e-26  # [use-standard-scientific-notation]
uppercase_e_wrong_small = 0.00012E-26  # [use-standard-scientific-notation]
wrong_negative_and_big = -10e3  # [use-standard-scientific-notation]
actual_trolling = 11000e26  # [use-standard-scientific-notation]
scientific_double_digit = 12e8  # [use-standard-scientific-notation]
scientific_triple_digit = 123e3  # [use-standard-scientific-notation]
zero_before_decimal_small = 0.0001e-5  # [use-standard-scientific-notation]
zero_before_decimal_big = 0.0001e5  # [use-standard-scientific-notation]
negative_decimal = -0.5e10  # [use-standard-scientific-notation]
zero_only = 0e10  # [use-standard-scientific-notation]

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
correct_small_exponent = 1.5e1
actually_nine = 9e0
actually_one = 1.0e0


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
complex_number_wrong = 15e3 + 25e3j  # [use-standard-scientific-notation]


#+1: [use-standard-scientific-notation, use-standard-scientific-notation]
def function_with_sci(param=10.0e3, other_param=20.0e3):
    return param, other_param

#+1: [use-standard-scientific-notation, use-standard-scientific-notation]
result = function_with_sci(20.0e3, 10.0e3)

valid_underscore_int = 1_000_000
valid_underscore_float = 1_000_000.12345
valid_underscore_float_exp = 123_000_000.12345e12_000_000 # [use-standard-scientific-notation]
valid_underscore_float_exp_cap = 123_000_000.12345E123_000_000 # [use-standard-scientific-notation]

invalid_underscore_octal = 0o123_456 # octal with underscores bypassed
invalid_underscore_hexa = 0x12c_456 # hexa with underscores bypassed

invalid_underscore_float_no_int = .123_456 # [esoteric-underscore-grouping]
invalid_underscore_float_no_frac = 123_456.123_456 # [esoteric-underscore-grouping]
incorrect_sci_underscore = 1.234_567e6 # [esoteric-underscore-grouping]
incorrect_sci_uppercase = 1.234_567E6 # [esoteric-underscore-grouping]
incorrect_sci_underscore_exp = 1.2e1_0  # [esoteric-underscore-grouping]
invalid_underscore_float = 1_234.567_89 # [esoteric-underscore-grouping]
invalid_underscore_binary = 0b1010_1010 # [esoteric-underscore-grouping]
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
wrong_big_underscore = 45.3_45e6
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
wrong_small_underscore = 0.000_12e-26
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
scientific_double_digit_underscore = 1_2e8
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
scientific_triple_digit_underscore = 12_3e3
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
invalid_underscore_sci = 1_234.567_89e10
invalid_underscore_sci_exp = 1.2e1_0 # [esoteric-underscore-grouping]
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
invalid_underscore_sci_combined = 1_2.3_4e5_6
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
invalid_uppercase_sci = 1_234.567_89E10
edge_underscore_1 = 1_0e6  # [use-standard-scientific-notation, esoteric-underscore-grouping]
mixed_underscore_1 = 1_000_000.0e-3  # [use-standard-scientific-notation]
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
mixed_underscore_2 = 0.000_001e3
mixed_underscore_3 = 1_0.0e2    # [use-standard-scientific-notation, esoteric-underscore-grouping]

# Complex numbers with underscores
complex_underscore = 1.5_6e3 + 2.5_6e3j # [esoteric-underscore-grouping]
#+1: [use-standard-scientific-notation, esoteric-underscore-grouping]
complex_underscore_wrong = 15_6e2 + 25_6e2j

#+2: [esoteric-underscore-grouping, esoteric-underscore-grouping]
#+1: [use-standard-scientific-notation, use-standard-scientific-notation]
def function_with_underscore(param=10.0_0e3, other_param=20.0_0e3):
    return param, other_param
