"""Tests for inconsistent quoting strategy.

In this file, double quotes are the majority quote delimiter.
"""

FIRST_STRING = "double-quoted string"
SECOND_STRING = 'single-quoted string' # [inconsistent-quotes]
THIRD_STRING = "another double-quoted string"
FOURTH_STRING = "yet another double-quoted string"
FIFTH_STRING = 'single-quoted string with an unescaped "double quote"'

def function_with_docstring():
    '''This is a multi-line docstring that should not raise a warning even though the
    delimiter it uses for quotes is not the delimiter used in the majority of the
    module.
    '''
