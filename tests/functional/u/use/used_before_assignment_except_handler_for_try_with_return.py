"""Tests for used-before-assignment with assignments in except handlers after
try blocks with return statements.
See: https://github.com/PyCQA/pylint/issues/5500.
"""
# pylint: disable=inconsistent-return-statements


def function():
    """Assume except blocks execute if the try block returns."""
    try:
        success_message = "success message"
        return success_message
    except ValueError:
        failure_message = "failure message"
    finally:
        print(failure_message)  # [used-before-assignment]

    return failure_message


def func_ok(var):
    """'msg' is defined in all ExceptHandlers."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        msg = "Attribute not defined"
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_ok2(var):
    """'msg' is defined in all ExceptHandlers that don't raise an Exception."""
    try:
        return 1 / var.some_other_func()
    except AttributeError as ex:
        raise Exception from ex
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_ok3(var):
    """'msg' is defined in all ExceptHandlers that don't return."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        return
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_ok4(var):
    """Define "msg" with a chained assignment."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        msg2 = msg = "Division by 0"
        print(msg2)
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_ok5(var):
    """Define 'msg' via unpacked iterable."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        msg, msg2 = ["Division by 0", "Division by 0"]
        print(msg2)
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)


def func_invalid1(var):
    """'msg' is not defined in one handler."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        pass
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)  # [used-before-assignment]


def func_invalid2(var):
    """'msg' is not defined in one handler."""
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        msg: str
    except ZeroDivisionError:
        msg = "Division by 0"
    print(msg)  # [used-before-assignment]


def func_invalid3(var):
    """'msg' is not defined in one handler, but is defined in another
    nested under an if. Nesting under an if tests that the implementation
    does not assume direct parentage between `msg=` and `except`, and
    the prior except is necessary to raise the message.
    """
    err_message = False
    try:
        return 1 / var.some_other_func()
    except AttributeError:
        pass
    except ZeroDivisionError:
        if err_message:
            msg = "Division by 0"
        else:
            msg = None
    print(msg)  # [used-before-assignment]
