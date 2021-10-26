"""Tests for undefined variable with assignment expressions"""
# pylint: disable=using-constant-test, expression-not-assigned

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

# Tests for assignment expressions in if ... else comprehensions


[i for i in range(10) if (if_assign_1 := i)]

print(if_assign_1)

IF_TWO = [i for i in range(10) if (if_assign_2 := i)]

print(if_assign_2)

IF_THREE = next(i for i in range(10) if (if_assign_3 := i))

print(if_assign_3)

IF_FOUR = {i: i for i in range(10) if (if_assign_4 := i)}

print(if_assign_4)

IF_FIVE = {i: i if (if_assign_5 := i) else 0 for i in range(10)}
print(if_assign_5)

{i: i if True else (else_assign_1 := i) for i in range(10)}

print(else_assign_1) # [undefined-variable]


# Tests for assignment expressions in the assignment of comprehensions

[(assign_assign_1 := i) for i in range(10)]

print(assign_assign_1)

COMPREHENSION_TWO =[(assign_assign_2 := i) for i in range(10)]

print(assign_assign_2)

COMPREHENSION_THREE = next((assign_assign_3 := i) for i in range(10))

print(assign_assign_3)

COMPREHENSION_FOUR = {i: (assign_assign_4 := i) for i in range(10)}

print(assign_assign_4)

COMPREHENSION_FIVE = {i: (else_assign_2 := i) if False else 0 for i in range(10)}

print(else_assign_2)  # [undefined-variable]
