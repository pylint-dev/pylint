# pylint: disable=missing-docstring,invalid-name

wrong_big = 45.3e6  # [use-standard-scientific-notation]
uppercase_e_wrong = 45.3E6  # [use-standard-scientific-notation]
wrong_small = 0.00012e-26  # [use-standard-scientific-notation]
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
correct_tiny_exponent = 9.0e0
correct_precise = 6.02214076e23

hex_constant = 0x1e4  # Hexadecimal, not scientific notation
binary_constant = 0b1010
octal_constant = 0o1234
inside_string = "Temperature: 10e3 degrees"
inside_multiline = """
This is a test with 45.3e6 inside
"""
inside_comment = 1.0  # This comment has 12e4 in it
in_variable_name = measurement_10e3 = 45
inside_f_string = f"Value is {1.0} not 10e6"

# Potential false negatives
barely_violation = 9.99e0  # Should this be 9.99?
integer_sci = int(1e10)  # Integer call with scientific notation
complex_number = 1.5e3 + 2.5e3j  # Complex number with scientific notation
tuple_of_sci = (1.2e4, 3.4e5)
list_of_sci = [5.6e6, 7.8e7]
dict_with_sci = {"a": 9.1e8, "b": 1.2e9}

# Mathematical operations
addition = 1.0e3 + 2.0e3
multiplication = 1.0e3 * 2.0
division = 1.0e3 / 2.0
power = 1.0e3 ** 2.0

# Function calls with scientific notation
def function_with_sci(param=1.0e3, other_param=2.0e3):
    return param, other_param

result = function_with_sci(2.0e3)
positional_and_keyword = function_with_sci(1.0, other_param=3.0e4)

# Assignments with operations
a = 1
a += 1.0e3
b = 2
b *= 2.0e3

# Scientific notation in different contexts
inside_list_comp = [x * 2 for x in [1.0e3, 2.0e3]]
inside_dict_comp = {str(x): x for x in [3.0e3, 4.0e3]}
inside_generator = (x + 1 for x in [5.0e3, 6.0e3])

# Boundary cases for normalization
boundary_small = 9.999e0  # Almost 10, but not quite
boundary_large = 1.001e0  # Just above 1
boundary_case = 1.0e0  # Equal to 1

# Constants from physics/science (correctly formatted)
speed_of_light = 2.99792458e8  # m/s
planck_constant = 6.62607015e-34  # J⋅s
electron_charge = 1.602176634e-19  # C
