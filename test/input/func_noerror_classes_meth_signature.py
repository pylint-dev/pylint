# pylint: disable=C0111,R0922,R0903
"""#2485
W0222 "Signature differs from overriden method" false positive
"""
__revision__ = 1
class Super(object):
    def method(self, param):
        raise NotImplementedError

class Sub(Super):
    def method(self, param = 'abc'):
        pass
