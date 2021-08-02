"""Test the superfluous-parens warning."""
from __future__ import print_function
# pylint: disable=unneeded-not, unnecessary-comprehension, missing-function-docstring
i = 3
if (i == 5):  # [superfluous-parens]
    pass
if not (i == 5):  # [superfluous-parens]
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

i = [x for x in ((3, 4))]  # [superfluous-parens]
i = [x for x in ((3, 4) if 1 > 0 else (5, 6))]
i = [x for x in ((3, 4) if 1 > 0 else ((5, 6)))]  # [superfluous-parens]
i = [x for x in ((3, 4) if 1 > 0 else ((((5, 6)))))]  # [superfluous-parens]


def a_function():
    return (x for x in ((3, 4)))  # [superfluous-parens]
