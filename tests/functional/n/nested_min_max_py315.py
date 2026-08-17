"""Tests for nested-min-max with PEP 798 starred comprehension elements."""
NESTED = [[1, 2], [3, 4]]
SMALLEST = min(1, min([*x for x in NESTED]))  # [nested-min-max, consider-using-generator]
