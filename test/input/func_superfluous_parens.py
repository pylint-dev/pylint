"""Test the superfluous-parens warning."""

__revision__ = 1

if (3 == 5):
    pass
if not (3 == 5):
    pass
if not (3 or 5):
    pass
for (x) in (1, 2, 3):
    print x
if (1) in (1, 2, 3):
    pass
if (1, 2) in (1, 2, 3):
    pass
DICT = {'a': 1, 'b': 2}
del(DICT['b'])
del DICT['a']
