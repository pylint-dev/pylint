# pylint: disable=missing-docstring, useless-return

def func():
    return None


SOME_VAR = func().DOES_NOT_EXIST # [no-member]
