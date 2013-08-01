"""test non-exceptions catched
"""

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

