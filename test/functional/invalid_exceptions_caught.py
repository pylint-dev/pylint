"""Test for catching non-exceptions."""
# pylint: disable=too-many-ancestors, print-statement, no-absolute-import
import socket

class MyException(object):
    """Custom 'exception'."""

class MySecondException(object):
    """Custom 'exception'."""

class MyGoodException(Exception):
    """Custom exception."""

class MySecondGoodException(MyGoodException):
    """Custom exception."""

class SkipException(socket.error):
    """Not an exception for Python 2, but one in 3."""

class SecondSkipException(SkipException):
    """Also a good exception."""

try:
    1 + 1
except MyException:  # [catching-non-exception]
    print "caught"

try:
    1 + 2
# +1:[catching-non-exception,catching-non-exception]
except (MyException, MySecondException):
    print "caught"

try:
    1 + 3
except MyGoodException:
    print "caught"

try:
    1 + 3
except (MyGoodException, MySecondGoodException):
    print "caught"

try:
    1 + 3
except (SkipException, SecondSkipException):
    print "caught"

try:
    1 + 42
# +1:[catching-non-exception,catching-non-exception]
except (None, list()):
    print "caught"

try:
    1 + 24
except None: # [catching-non-exception]
    print "caught"

EXCEPTION = None
EXCEPTION = ZeroDivisionError
try:
    1 + 46
except EXCEPTION:
    print "caught"
