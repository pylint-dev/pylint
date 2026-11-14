"""Tests for use-a-generator with PEP 798 starred comprehension elements."""
NESTED = [[True], [False]]
ANY = any([*x for x in NESTED])  # [use-a-generator]
ALL = all([*x for x in NESTED])  # [use-a-generator]
