"""Regression test for trailing-whitespace (C0303)."""
# pylint: disable=mixed-line-endings,pointless-string-statement

# +1: [trailing-whitespace]
print('some trailing whitespace')   
# +1: [trailing-whitespace]
print('trailing whitespace does not count towards the line length limit')                   
print('windows line ends are ok')
# +1: [trailing-whitespace]
print('but trailing whitespace on win is not')   

# Regression test for https://github.com/pylint-dev/pylint/issues/6936
# +2: [trailing-whitespace]
""" This module has the Board class.
""" 

# +3: [trailing-whitespace]
""" This module has the Board class.
It's a very nice Board.
""" 

# Regression test for https://github.com/pylint-dev/pylint/issues/3822
def example(*args):
    """Example function."""
    print(*args)


example(
    "bob", """
    foobar 
    more text
""",
)

example(
    "bob",
    """
    foobar2 
    more text
""",
)
