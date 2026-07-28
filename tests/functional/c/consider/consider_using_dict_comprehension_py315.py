"""Tests for consider-using-dict-comprehension with PEP 798 starred elements.

``dict([*kv for kv in PAIRS])`` flattens the pair lists, so the equivalent
comprehension is ``{**dict(kv) for kv in PAIRS}`` rather than a plain
key/value comprehension.
"""
PAIRS = [[("a", 1)], [("b", 2)]]
MERGED = dict([*kv for kv in PAIRS])  # [consider-using-dict-comprehension]
