# pylint: disable=R0903, C0111, W0231
"""test external access to protected class members"""

__revision__ = ''

class MyClass(object):
    _cls_protected = 5

    def __init__(self, other):
        MyClass._cls_protected = 6
        self._protected = 1
        self.public = other
        self.attr = 0

    def test(self):
        self._protected += self._cls_protected
        print self.public._haha

    def clsmeth(cls):
        cls._cls_protected += 1
        print cls._cls_protected
    clsmeth = classmethod(clsmeth)

class Subclass(MyClass):

    def __init__(self):
        MyClass._protected = 5

INST = Subclass()
INST.attr = 1
print INST.attr
INST._protected = 2
print INST._protected
INST._cls_protected = 3
print INST._cls_protected

