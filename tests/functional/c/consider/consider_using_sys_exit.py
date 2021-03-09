# pylint: disable=missing-docstring, invalid-name, disallowed-name, redefined-builtin, unused-variable
import sys

def foo():
    exit()  # [consider-using-sys-exit]

def foo_1():
    quit()  # [consider-using-sys-exit]

def foo_2():
    quit = 'abc'
    sys.exit()

quit()  # [consider-using-sys-exit]
