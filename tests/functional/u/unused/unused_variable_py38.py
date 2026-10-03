"""Tests for the unused-variable message in assignment expressions"""


def typed_assignment_in_function_default( # [unused-variable]
    param: str = (typed_default := "walrus"),  # [unused-variable]
) -> None:
    """An unused annotated assignment expression in a default parameter should emit"""
    return param


def assignment_in_function_default( # [unused-variable]
    param=(default := "walrus"),  # [unused-variable]
) -> None:
    """An unused assignment expression in a default parameter should emit"""
    return param


def assignment_used_in_function_scope( # [unused-variable]
    param=(function_default := "walrus"),
) -> None:
    """An used assignment expression in a default parameter should not emit"""
    print(function_default)
    return param


def assignment_used_in_global_scope( # [unused-variable]
    param=(global_default := "walrus"),
) -> None:
    """An used assignment expression in a default parameter should not emit"""
    return param

print(global_default)
