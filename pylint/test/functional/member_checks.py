# pylint: disable=print-statement,missing-docstring,no-self-use,too-few-public-methods
"""check getattr if inference succeed"""
from __future__ import print_function

class Provider(object):
    """provide some attributes and method"""
    cattr = 4
    def __init__(self):
        self.attr = 4
    def method(self, val):
        """impressive method"""
        return self.attr * val
    def hophop(self):
        """hop method"""
        print('hop hop hop', self)


class Client(object):
    """use provider class"""

    def __init__(self):
        self._prov = Provider()
        self._prov_attr = Provider.cattr
        self._prov_attr2 = Provider.cattribute  # [no-member]
        self.set_later = 0

    def set_set_later(self, value):
        """set set_later attribute (introduce an inference ambiguity)"""
        self.set_later = value

    def use_method(self):
        """use provider's method"""
        self._prov.hophop()
        self._prov.hophophop()  # [no-member]

    def use_attr(self):
        """use provider's attr"""
        print(self._prov.attr)
        print(self._prov.attribute)  # [no-member]

    def debug(self):
        """print debug information"""
        print(self.__class__.__name__)
        print(self.__doc__)
        print(self.__dict__)
        print(self.__module__)

    def test_bt_types(self):
        """test access to unexistant member of builtin types"""
        lis = []
        lis.apppend(self)  # [no-member]
        dic = {}
        dic.set(self)  # [no-member]
        tup = ()
        tup.append(self)  # [no-member]
        string = 'toto'
        print(string.loower())  # [no-member]
        integer = 1
        print(integer.whatever)  # [no-member]

    def test_no_false_positives(self):
        none = None
        print(none.whatever)
        # This will be handled when we'll understand super
        super(Client, self).misssing()


class Mixin(object):
    """No no-member should be emitted for mixins."""

class Getattr(object):
    """no-member shouldn't be emitted for classes with dunder getattr."""

    def __getattr__(self, attr):
        return self.__dict__[attr]


class Getattribute(object):
    """no-member shouldn't be emitted for classes with dunder getattribute."""

    def __getattribute__(self, attr):
        return 42

print(object.__init__)
print(property.__init__)
print(Client().set_later.lower())  # [no-member]
print(Mixin().nanana())
print(Getattr().nananan())
print(Getattribute().batman())
