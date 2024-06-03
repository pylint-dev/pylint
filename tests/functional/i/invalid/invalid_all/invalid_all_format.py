"""Test invalid __all__ format.

Tuples with one element MUST contain a comma! Otherwise it's a string.
"""
__all__ = ("CONST")  # [invalid-all-format, superfluous-parens]

CONST = 42
