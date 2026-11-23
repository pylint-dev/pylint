# Regression test for https://github.com/pylint-dev/pylint/issues/8746
# Fixed with astroid 4.3.0: no more crash when a functional namedtuple field
# name changes under NFKC normalization ("µ" MICRO SIGN becomes "μ" GREEK MU).
"""Crash regression test for namedtuple fields normalized by NFKC."""
from collections import namedtuple

NAMES = ["µ"]
Micro = namedtuple("Micro", NAMES)
