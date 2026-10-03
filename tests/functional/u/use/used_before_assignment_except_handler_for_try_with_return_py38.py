"""Tests for used-before-assignment with assignments in except handlers after
try blocks with return statements.
See: https://github.com/pylint-dev/pylint/issues/5500.
"""
# pylint: disable=inconsistent-return-statements


# Named expressions
def func_ok_namedexpr_1(var):
    """'msg' is defined in one handler with a named expression under an if."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        if (msg := var.get_msg()):
            pass
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_ok_namedexpr_2(var):
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


def func_ok_namedexpr_3(var):
    """'msg' is defined in one handler with a named expression occurring
    as a keyword in a call used in an if test.
    """
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        if print("zero!", "here", sep=(msg := var.get_sep())):
            pass
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)
