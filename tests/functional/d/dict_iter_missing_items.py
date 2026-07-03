# pylint: disable=invalid-name, consider-iterating-dictionary, missing-docstring, import-error
from unknown import Uninferable

d = {1: 1, 2: 2}
d_tuple = {(1, 2): 3, (4, 5): 6}
l = [1, 2]
s1 = {1, 2}
s2 = {1, 2, 3}

# Positive
for k, v in d:  # [dict-iter-missing-items]
    pass

# Negative
for k, v in d.items():
    pass
for k in d.keys():
    pass
for i, v in enumerate(l):
    pass
for i, v in s1.intersection(s2):
    pass
for k, v in Uninferable:
    pass
for a, b in d_tuple:
    pass
