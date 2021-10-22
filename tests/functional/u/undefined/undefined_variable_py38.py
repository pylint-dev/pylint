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


# pylint: disable-next=fixme
# TODO: With better control-flow inference related to NamedExpr we should see that the
# NamedExpr is never called here and the second call to `var` is thus undefined
def typing_and_incorrect_assignment_expression():
    """The variable gets assigned in an assignment expression which is never called"""
    var: int
    if False:
        if (var := 1 ** 2):
            print(var)
    else:
        print(var)
