"""W0107: unnecessary pass statement
"""
from __future__ import print_function

try:
    A = 2
except ValueError:
    print(A)
    pass
