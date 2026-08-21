"""Tests for consider-using-dict-comprehension with PEP 798 starred elements.

``dict([*kv for kv in PAIRS])`` flattens the pair lists, so it is not
equivalent to a key/value dict comprehension and must not be reported.
"""
PAIRS = [[("a", 1)], [("b", 2)]]
MERGED = dict([*kv for kv in PAIRS])
REPORTED = dict([(k, k * 2) for k in [1, 2]])  # [consider-using-dict-comprehension]
