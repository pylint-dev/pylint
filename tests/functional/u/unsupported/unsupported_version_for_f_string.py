"""Tests for the use of f-strings whenever the py-version is set < 3.6"""
# pylint: disable=f-string-without-interpolation

VAR = f"a simple f-string"  # [using-f-string-in-unsupported-version]
VAR_TWO = f"a simple f-string {'with'} interpolation"  # [using-f-string-in-unsupported-version]
