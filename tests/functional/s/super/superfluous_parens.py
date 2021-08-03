"""Test the superfluous-parens warning."""
from __future__ import print_function
# pylint: disable=unneeded-not, unnecessary-comprehension, missing-function-docstring, invalid-name
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

B = [x for x in ((3, 4))]  # [superfluous-parens]
C = [x for x in ((3, 4) if 1 > 0 else (5, 6))]
D = [x for x in ((3, 4) if 1 > 0 else ((5, 6)))]  # [superfluous-parens]
E = [x for x in ((3, 4) if 1 > 0 else ((((5, 6)))))]  # [superfluous-parens]

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

# Test functions
def function_A():
    return (x for x in ((3, 4)))  # [superfluous-parens]
