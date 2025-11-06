"""Test module-level constants with class attribute same name
Regression test for #10719.
"""
# pylint: disable=missing-docstring, too-few-public-methods, redefined-builtin


class Theme:
    INPUT = ">>> "


INPUT = Theme()
input = Theme()
OUTPUT = Theme()
output = Theme()
