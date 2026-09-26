"""Regression test for a crash with non-numeric slice bounds in a for loop.

See issue #11472.
"""

# pylint: disable=missing-docstring,unused-variable,unbalanced-tuple-unpacking,unbalanced-dict-unpacking

# +1: [invalid-slice-index]
for _a, _b in {"k": [][0:""]}.values():  # noqa: RUF016
    pass

x = [1, 2, 3]
lo, hi = 1, 2

for _a, _b in {"k": x[lo:hi]}.values():
    pass

# +1: [invalid-slice-step]
for _a, _b in {"k": x[0:10:0]}.values():
    pass
