"""Check various forms of strings which could be f-strings without a prefix"""
# pylint: disable=invalid-name, line-too-long, pointless-string-statement, pointless-statement
# pylint: disable=missing-function-docstring

# Check for local variable interpolation
PARAM = "string"
PARAM_TWO = "extra string"

A = f"This is a {PARAM} which should be a f-string"
B = "This is a {PARAM} used twice, see {PARAM}"
C = "This is a {PARAM} which should be a f-string"  # [possible-forgotten-f-prefix]
D = "This is a {PARAM} and {PARAM_TWO} which should be a f-string"  # [possible-forgotten-f-prefix, possible-forgotten-f-prefix]
E1, E2, E3 = (1, 2, "This is a {PARAM} which should be a f-string")  # [possible-forgotten-f-prefix]

# Check for use of .format()
F = "This is a {parameter} used for formatting later"
G = F.format(parameter="string")

H = "This is a {another_parameter} used for formatting later"
I = H.format(another_parameter="string")

# Check for use of variables within functions
PARAM_LIST = [PARAM, PARAM_TWO]
J = f"This is an example with a list: {''.join(PARAM_LIST) + 'well...'}"
K = "This is an example with a list: {''.join(PARAM_LIST) + 'well...'}"  # [possible-forgotten-f-prefix]

# Check for calculations without variables
L = f"This is a calculation: {1 + 1}"
M = "This is a calculation: {1 + 1}"  # [possible-forgotten-f-prefix]

# Check invalid Python code
N = "This is {invalid /// python /// inside}"
O = "This is {not */ valid python.}"
P = "This is {def function(): return 42} valid python but not an expression"




# Check strings without assignment
PARAM_THREE = "string"
f"This is a {PARAM_THREE}"
"This is a string"
"This is a {PARAM_THREE}"  # [possible-forgotten-f-prefix]

f"This is a calculation: {1 + 1}"
"This is a calculation: 1 + 1"
"This is a calculation: {1 + 1}"  # [possible-forgotten-f-prefix]

f"This is a {'nice' + PARAM_THREE}"
"This is a nice string"
"This is a {'nice' + PARAM_THREE}"  # [possible-forgotten-f-prefix]
