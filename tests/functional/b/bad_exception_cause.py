"""Check that raise ... from .. uses a proper exception cause """

# pylint: disable=unreachable, import-error, multiple-imports

import socket, unknown


class ExceptionSubclass(Exception):
    """ subclass """

def test():
    """ docstring """
    raise IndexError from 1 # [bad-exception-cause]
    raise IndexError from None
    raise IndexError from ZeroDivisionError
    raise IndexError from object() # [bad-exception-cause]
    raise IndexError from ExceptionSubclass
    raise IndexError from socket.error
    raise IndexError() from None
    raise IndexError() from ZeroDivisionError
    raise IndexError() from ZeroDivisionError()
    raise IndexError() from object() # [bad-exception-cause]
    raise IndexError() from unknown

def unknown_bases():
    """Don't emit when a base of the cause's class could not be inferred."""
    from lala import bala  # pylint: disable=import-outside-toplevel

    class MyException(bala):
        """Whether this derives from BaseException cannot be determined."""

    try:
        pass
    except MyException as exc:
        raise IndexError from exc


def function():
    """Function to be passed as exception"""

try:
    pass
except function as exc:  # [catching-non-exception]
    raise Exception from exc  # [bad-exception-cause, broad-exception-raised]
