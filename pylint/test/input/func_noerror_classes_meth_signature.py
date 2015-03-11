# pylint: disable=C0111,R0903,W0231
"""#2485:
W0222 "Signature differs from overriden method" false positive
#18772:
no prototype consistency check for mangled methods
"""
__revision__ = 1
class Super(object):
    def __init__(self):
        pass

    def __private(self):
        pass

    def __private2_(self):
        pass

    def ___private3(self):
        pass

    def method(self, param):
        raise NotImplementedError

class Sub(Super):
    def __init__(self, arg):
        pass

    def __private(self, arg):
        pass

    def __private2_(self, arg):
        pass

    def ___private3(self, arg):
        pass

    def method(self, param='abc'):
        pass
