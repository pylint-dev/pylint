"""Regression test for trailing-whitespace (C0303)."""
# pylint: disable=mixed-line-endings
from __future__ import print_function

print('some trailing whitespace')   
print('trailing whitespace does not count towards the line length limit')                   
print('windows line ends are ok')
print('but trailing whitespace on win is not')   
