# pylint: disable=too-few-public-methods, W0231, print-statement
"""Test external access to protected class members."""


class MyClass(object):
    """Class with protected members."""
    _cls_protected = 5

    def __init__(self, other):
        MyClass._cls_protected = 6
        self._protected = 1
        self.public = other
        self.attr = 0

    def test(self):
        """Docstring."""
        self._protected += self._cls_protected
        print self.public._haha  # [protected-access]

    def clsmeth(cls):
        """Docstring."""
        cls._cls_protected += 1
        print cls._cls_protected
    clsmeth = classmethod(clsmeth)

class Subclass(MyClass):
    """Subclass with protected members."""

    def __init__(self):
        MyClass._protected = 5

INST = Subclass()
INST.attr = 1
print INST.attr
INST._protected = 2  # [protected-access]
print INST._protected  # [protected-access]
INST._cls_protected = 3  # [protected-access]
print INST._cls_protected  # [protected-access]
