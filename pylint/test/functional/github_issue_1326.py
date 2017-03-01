"""
https://github.com/PyCQA/pylint/issues/1326
"""
from __future__ import print_function
import socket

RETRYABLE_EXCEPTIONS = (socket.error,)

try:
    print("hello")
except RETRYABLE_EXCEPTIONS + tuple():
    print("exception caught")
