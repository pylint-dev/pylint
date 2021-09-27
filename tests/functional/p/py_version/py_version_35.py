"""Test warnings aren't emitted for features that require Python > 3.5"""
# pylint: disable=invalid-name

# consider-using-f-string -> requires Python 3.6
"Hello {}".format("World")


# ------
# CodeStyle extension

# consider-using-assignment-expr -> requires Python 3.8
a1 = 2
if a1:
    ...
