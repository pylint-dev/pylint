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


def typed_assignment_in_function_default(param: str = (typed_default := "walrus")) -> None:
    """An annotated assignment expression in a default parameter should not emit"""
    return param


print(typed_default)


def assignment_in_function_default(param = (default := "walrus")) -> None:
    """An assignment expression in a default parameter should not emit"""
    return param


print(default)


def no_assignment_in_function_default(param: str = "walrus") -> None:
    """No annotated assignment expression should emit"""
    return param


print(no_default) # [undefined-variable]


def no_parameters_in_function_default() -> None:
    """Regression tests for functions without any parameters"""
    return


print(again_no_default) # [undefined-variable]
