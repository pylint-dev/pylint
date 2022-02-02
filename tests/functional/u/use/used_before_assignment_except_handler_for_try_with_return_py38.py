"""Tests for used-before-assignment with assignments in except handlers after
try blocks with return statements.
See: https://github.com/PyCQA/pylint/issues/5500.
"""
# pylint: disable=inconsistent-return-statements


# Intended to follow func_ok1 ... 3 in neighboring file
def func_ok4(var):
    """'msg' is defined in one handler with a named expression under an if."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        if (msg := var.get_msg()):
            pass
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_ok5(var):
    """'msg' is defined in one handler with a named expression occurring
    in a call used in an if test.
    """
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        if print(msg := var.get_msg()):
            pass
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)
