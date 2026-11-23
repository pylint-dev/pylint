"""Tests for consider-using-generator with PEP 798 starred comprehension elements."""
NESTED = [[1, 2], [3, 4]]
TOTAL = sum([*x for x in NESTED])  # [consider-using-generator]
AS_TUPLE = tuple([*x for x in NESTED])  # [consider-using-generator]
