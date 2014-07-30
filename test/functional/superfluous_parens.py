"""Test the superfluous-parens warning."""


if (3 == 5):  # [superfluous-parens]
    pass
if not (3 == 5):  # [superfluous-parens]
    pass
if not (3 or 5):
    pass
for (x) in (1, 2, 3):  # [superfluous-parens]
    print x
if (1) in (1, 2, 3):  # [superfluous-parens]
    pass
if (1, 2) in (1, 2, 3):
    pass
DICT = {'a': 1, 'b': 2}
del(DICT['b'])  # [superfluous-parens]
del DICT['a']
