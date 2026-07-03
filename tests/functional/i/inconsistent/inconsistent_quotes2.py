"""Tests for inconsistent quoting strategy.

In this file, single quotes are the majority quote delimiter.
"""

FIRST_STRING = "double-quoted string"  # [inconsistent-quotes]
SECOND_STRING = 'single-quoted string'
THIRD_STRING = 'another single-quoted string'
FOURTH_STRING = 'yet another single-quoted string'
FIFTH_STRING = "double-quoted string with an unescaped 'single quote'"
