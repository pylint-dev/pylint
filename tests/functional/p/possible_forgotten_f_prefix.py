"""Check various forms of strings which could be f-strings without a prefix"""
# pylint: disable=invalid-name, line-too-long, pointless-string-statement, pointless-statement
# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods
# pylint: disable=useless-object-inheritance

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
F.format(parameter="string")
G = F.format(parameter="string")
"{0}, {1}".format(1, 2)
H = "{0}, {1}".format(1, 2)
I1, I2, I3 = (1, 2, "This is a {PARAM} which is later formatted")
I3.format(PARAM=PARAM)

J = {"key_one": "", "key_two": {"inner_key": ""}}
J["key_one"] = "This is a {parameter} used for formatting later"
J["key_one"].format(parameter=PARAM)
K = J["key_one"].format(parameter=PARAM)
J["key_two"]["inner_key"] = "This is a {parameter} used for formatting later"
J["key_two"]["inner_key"].format(parameter=PARAM)
L = J["key_two"]["inner_key"].format(parameter=PARAM)

M = "This is a {parameter} used for formatting later"

def func_one():
    return "{0}, {1}".format(1, 2)


def func_two():
    x = "{0}, {1}"
    return x.format(1, 2)


def func_three():
    x = M.format(parameter=PARAM)
    return x

class Class(object):
    attr = 0

    def __str__(self):
        return "{self.attr}".format(self=self)


# Check for use of variables within functions
PARAM_LIST = [PARAM, PARAM_TWO]
N = f"This is an example with a list: {''.join(PARAM_LIST) + 'well...'}"
O = "This is an example with a list: {''.join(PARAM_LIST) + 'well...'}"  # [possible-forgotten-f-prefix]

# Check for calculations without variables
P = f"This is a calculation: {1 + 1}"
Q = "This is a calculation: {1 + 1}"  # [possible-forgotten-f-prefix]

# Check invalid Python code
R = "This is {invalid /// python /// inside}"
S = "This is {not */ valid python.}"
T = "This is {def function(): return 42} valid python but not an expression"

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

# Check raw strings
U = r"a{1}"
