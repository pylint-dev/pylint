"""No warnings should be emitted for features that require Python > 3.5"""
# pylint: disable=invalid-name

# consider-using-assignment-expr -> requires Python 3.8
a1 = 2
if a1:
    ...
