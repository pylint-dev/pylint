# pylint: disable=missing-docstring

import socket

RETRYABLE_EXCEPTIONS = (socket.error,)

# pylint: disable=wrong-exception-operation
def exception_handler():
    try:
        yield 1
    except RETRYABLE_EXCEPTIONS + tuple():
        yield 2
