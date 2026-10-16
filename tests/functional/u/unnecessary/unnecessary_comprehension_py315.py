"""PEP 798 comprehension unpacking is never an unnecessary-comprehension."""
NESTED = [[1, 2], [3, 4]]
DICTS = [{"a": 1}, {"b": 2}]
FLAT = [*x for x in NESTED]
MERGED = {**d for d in DICTS}
COPIED = [x for x in NESTED]  # [unnecessary-comprehension]
