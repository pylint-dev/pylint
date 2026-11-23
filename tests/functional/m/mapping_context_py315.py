"""PEP 798 unpacking checks that the unpacked element is a mapping."""
MAPPINGS = [{"a": 1}, {"b": 2}]
NUMBERS = [1, 2, 3]

MERGED = {**mapping for mapping in MAPPINGS}

BAD_MERGED = {**number for number in NUMBERS}  # [not-a-mapping]
