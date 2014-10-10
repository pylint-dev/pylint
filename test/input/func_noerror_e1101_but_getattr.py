"""don't want E1101 if __getattr__ is defined"""
from __future__ import print_function
__revision__ = None

class MyString(object):
    """proxied string"""

    def __init__(self, string):
        self.string = string

    def __getattr__(self, attr):
        return getattr(self.string, attr)

    def lower(self):
        """string.lower"""
        return self.string.lower()

    def upper(self):
        """string.upper"""
        return self.string.upper()

MYSTRING = MyString("abc")
print(MYSTRING.title())
