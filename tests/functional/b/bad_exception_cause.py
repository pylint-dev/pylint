"""Check that raise ... from .. uses a proper exception context """

# pylint: disable=unreachable, import-error, multiple-imports

import socket, unknown

__revision__ = 0

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

def function():
    """Function to be passed as exception"""

try:
    pass
except function as exc:  # [catching-non-exception]
    raise Exception from exc  # [bad-exception-cause]
