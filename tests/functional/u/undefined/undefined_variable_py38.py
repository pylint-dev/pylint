"""Tests for undefined variable with assignment expressions"""
# pylint: disable=using-constant-test

# Tests for annotation of variables and potentially undefinition

def typing_and_assignment_expression():
    """The variable gets assigned in an assignment expression"""
    var: int
    if (var := 1 ** 2):
        print(var)


def typing_and_self_referncing_assignment_expression():
    """The variable gets assigned in an assignment expression that references itself"""
    var: int
    if (var := var ** 2): # [undefined-variable]
        print(var)
