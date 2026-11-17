# pylint: disable=invalid-name, missing-docstring
"""Implicit concatenation of t-strings (#8968)."""

a = 1
b = 2

templates = [t"{a} = " t"{b}."]  # [implicit-str-concat]
print(t"{a}" t"{b}")  # [implicit-str-concat]
assigned = t"{a}" t"{b}"  # [implicit-str-concat]

single = t"{a}"
separated = (t"{a}", t"{b}")
print(t"{a}", t"{b}")
