"""Test the superfluous-parens warning."""
# pylint: disable=unneeded-not, unnecessary-comprehension, missing-function-docstring, invalid-name, fixme
# pylint: disable=import-error, missing-class-docstring, too-few-public-methods
import numpy as np
A = 3
if (A == 5):  # [superfluous-parens]
    pass
if not (A == 5):  # [superfluous-parens]
    pass
if not (3 or 5):
    pass
for (x) in (1, 2, 3):  # [superfluous-parens]
    print(x)
if (1) in (1, 2, 3):  # [superfluous-parens]
    pass
if (1, 2) in (1, 2, 3):
    pass
DICT = {'a': 1, 'b': 2}
del(DICT['b'])  # [superfluous-parens]
del DICT['a']

B = [x for x in ((3, 4))]
C = [x for x in ((3, 4) if 1 > 0 else (5, 6))]  # pylint: disable=comparison-of-constants
D = [x for x in ((3, 4) if 1 > 0 else ((5, 6)))]  # pylint: disable=comparison-of-constants
E = [x for x in ((3, 4) if 1 > 0 else ((((5, 6)))))]  # pylint: disable=comparison-of-constants

# Test assertions
F = "Version 1.0"
G = "1.0"
assert "Version " + G in F
assert ("Version " + G) in F # [superfluous-parens]

# Test assignment
H = 2 + (5 * 3)
NUMS_LIST = ['1', '2', '3']
NUMS_SET = {'1', '2', '3'}
NUMS_DICT = {'1': 1, '2': 2, '3': 3}
I = tuple(x for x in ((a, str(a)) for a in ()))

# Test functions
def function_A():
    return (x for x in ((3, 4)))

def function_B(var):
    return (var.startswith(('A', 'B', 'C')) or var == 'D')

def function_C(first, second):
    return (first or second) in (0, 1)

# TODO: Test string combinations, see https://github.com/PyCQA/pylint/issues/4792
# The lines with "+" should raise the superfluous-parens message
J = "TestString"
K = ("Test " + "String")
L = ("Test " + "String") in I
assert "" + ("Version " + "String") in I

# Test numpy
def function_numpy_A(var_1: int, var_2: int) -> np.ndarray:
    result = (((var_1 & var_2)) > 0)
    return result.astype(np.float32)

def function_numpy_B(var_1: int, var_2: int) -> np.ndarray:
    return (((var_1 & var_2)) > 0).astype(np.float32)

# Test Class
class ClassA:
    keys = []

    def __iter__(self):
        return ((k, getattr(self, k)) for k in self.keys)

if (A == 2) is not (B == 2):
    pass

M = A is not (A <= H)
M = True is not (M == K)
M = True is not (True is not False)  # pylint: disable=comparison-of-constants
