"""Tests for use-implicit-booleaness-not-len with PEP 798 starred elements."""
NESTED = [[1, 2], [3, 4]]
if len([*x for x in NESTED]):  # [use-implicit-booleaness-not-len]
    pass
