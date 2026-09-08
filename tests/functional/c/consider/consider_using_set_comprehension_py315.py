"""Tests for consider-using-set-comprehension with PEP 798 starred elements."""
NESTED = [[1, 2], [3, 4]]
FLAT = set([*x for x in NESTED])  # [consider-using-set-comprehension]
