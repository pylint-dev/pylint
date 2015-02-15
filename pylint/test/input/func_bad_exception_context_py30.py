"""Check that raise ... from .. uses a proper exception context """

# pylint: disable=unreachable, import-error

import socket, unknown

__revision__ = 0

class ExceptionSubclass(Exception):
    """ subclass """

def test():
    """ docstring """
    raise IndexError from 1
    raise IndexError from None
    raise IndexError from ZeroDivisionError
    raise IndexError from object()
    raise IndexError from ExceptionSubclass
    raise IndexError from socket.error
    raise IndexError() from None
    raise IndexError() from ZeroDivisionError
    raise IndexError() from ZeroDivisionError()
    raise IndexError() from object()
    raise IndexError() from unknown
