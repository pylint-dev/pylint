"""Test the superfluous-parens warning with python 3.8 functionality (walrus operator)"""
# pylint: disable=missing-function-docstring
if not (x := False):
    print(x)

if not ((x := 1)):  # [superfluous-parens]
    pass

if not ((((x := 1)))):  # [superfluous-parens]
    pass
