"""test non-exceptions catched
"""
import socket

__revision__ = 1

class MyException(object):
    """ custom 'exception' """
    pass

class MySecondException(object):
    """ custom 'exception' """
    pass

class MyGoodException(Exception):
    """ custom 'exception' """
    pass

class MySecondGoodException(MyGoodException):
    """ custom 'exception' """
    pass

class SkipException(socket.error):
    """ This gave false positives for Python 2,
    but not for Python 3, due to exception
    hierarchy rewrite.
    """

class SecondSkipException(SkipException):
    """ This too shouldn't give false
    positives. """

try:
    1 + 1
except MyException:
    print "oups"

try:
    1 + 2
except (MyException, MySecondException):
    print "oups"

try:
    1 + 3
except MyGoodException:
    print "should work"

try:
    1 + 3
except (MyGoodException, MySecondGoodException):
    print "should work"

try:
    1 + 3
except (SkipException, SecondSkipException):
    print "should work"
