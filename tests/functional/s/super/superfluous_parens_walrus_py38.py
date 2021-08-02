"""Test the superfluous-parens warning with python 3.8 functionality (walrus operator)"""
# pylint: disable=missing-function-docstring,invalid-name
if not (x := False):
    print(x)

if not ((x := 1)):  # [superfluous-parens]
    pass

if not ((((x := 1)))):  # [superfluous-parens]
    pass

i = 1
y = 1

if odd := is_odd(i): # [undefined-variable]
    pass
if not (foo := 5):
    pass

if not ((x := y)):  # [superfluous-parens]
    pass

if ((x := y)):   # [superfluous-parens]
    pass
