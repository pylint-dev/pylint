"""Test if disable-next only disables messages for the next line"""
# pylint: disable=missing-function-docstring
# pylint: disable-next=unused-argument, invalid-name
def function_A(arg1, arg2):
    return arg1


# pylint: disable-next=unused-argument,invalid-name
def function_B(arg1, arg2):
    return arg1


# pylint: disable-next=invalid-name, f-string-without-interpolation
def function_C():
    X = "string"  # [unused-variable, invalid-name]
    return f"This should be a normal string"  # [f-string-without-interpolation]


def function_D(arg1, arg2):  # [unused-argument, invalid-name]
    return arg1


def function_E():  # [invalid-name]
    # pylint: disable-next=unused-variable

    test = 43  # [unused-variable]
    blah = 123  # [unused-variable]
