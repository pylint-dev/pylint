"""Test for cython pure Python false positives"""
import cython

# cython allows any import in pure Python mode. It can only
# be determined correct at compile time
# Check that it raises neither an import-error nor a
# no-name-in-module error
from cython.cimports.libc.math import sin

# Same with type declarations
# Check it doesn't generate a no-member error
MY_VAR = cython.declare(cython.int, 0)
print(sin(MY_VAR))
