"""import as non ascii alias"""
from os.path import join as łos  # [non-ascii-name]


# Usage should not raise a second error
foo = łos("a", "b")
