"""Warnings about global statements and usage of global variables."""
# pylint: disable=invalid-name, redefined-outer-name, missing-function-docstring, import-outside-toplevel
from __future__ import print_function

global CSTE  # [global-at-module-level]
print(CSTE)  # [undefined-variable]

CONSTANT = 1
def FUNC():
    pass

def fix_contant(value):
    """all this is ok, but try not using global ;)"""
    global CONSTANT  # [global-statement]
    print(CONSTANT)
    CONSTANT = value


def other():
    """global behaviour test"""
    global HOP  # [global-variable-not-assigned]
    print(HOP)  # [undefined-variable]


def define_constant():
    """ok but somevar is not defined at the module scope"""
    global SOMEVAR  # [global-variable-undefined]
    SOMEVAR = 2


def global_with_import():
    """should only warn for global-statement"""
    global sys  # [global-statement]
    import sys  # pylint: disable=import-outside-toplevel


def global_no_assign():
    """Not assigning anything to the global makes 'global' superfluous"""
    global CONSTANT  # [global-variable-not-assigned]
    print(CONSTANT)


def global_operator_assign():
    """Operator assigns should only throw a global statement error"""
    global CONSTANT  # [global-statement]
    print(CONSTANT)
    CONSTANT += 1


def global_function_assign():
    """Function assigns should only throw a global statement error"""
    global CONSTANT  # [global-statement]

    def CONSTANT():
        pass

    CONSTANT()


def override_func():
    """Overriding a function should only throw a global statement error"""
    global FUNC # [global-statement]

    def FUNC():
        pass

    FUNC()

def func():
    """Overriding a global with an import should only throw a global statement error"""
    global sys  # [global-statement]

    import sys
