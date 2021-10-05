"""Emit a message for explict usage of collection literals."""
# pylint: disable=missing-docstring, invalid-name
# https://github.com/PyCQA/pylint/issues/4774

test = []
if test == []: # [use-implicit-booleanness]
    test.append(1)

if [] == test: # [use-implicit-booleanness]
    test.append(1)

def function_test() -> bool:
    return [] == test # [use-implicit-booleanness]

def function_test3() -> bool:
    return test == [] # [use-implicit-booleanness]
