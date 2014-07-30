"""Test for catching non-exceptions."""
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
