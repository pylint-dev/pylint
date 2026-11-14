"""Tests for undefined-variable in PEP 798 starred comprehension elements."""
NESTED = [[1, 2], [3, 4]]
FLAT = [*x for x in NESTED]
BAD = [*missing for x in NESTED]  # [undefined-variable]
