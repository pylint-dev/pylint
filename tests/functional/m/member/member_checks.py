# pylint: disable=print-statement,missing-docstring,no-self-use,too-few-public-methods,bare-except,broad-except, useless-object-inheritance, unused-private-member
# pylint: disable=using-constant-test,expression-not-assigned, assigning-non-slot, unused-variable,pointless-statement, wrong-import-order, wrong-import-position,import-outside-toplevel
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
        # No misssing in the parents.
        super().misssing() # [no-member]


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
print(Client().set_later.lower())
print(Mixin().nanana())
print(Getattr().nananan())
print(Getattribute().batman())

try:
    Client().missing_method()
except AttributeError:
    pass

try:
    Client().indeed() # [no-member]
except ImportError:
    pass

try:
    Client.missing()
except AttributeError:
    Client.missing() # [no-member]

try:
    Client.missing()
except AttributeError:
    try:
        Client.missing() # [no-member]
    except ValueError:
        pass

try:
    if Client:
        Client().missing()
except AttributeError:
    pass

try:
    Client().indeed()
except AttributeError:
    try:
        Client.missing() # [no-member]
    except Exception:
        pass


class SuperChecks(str, str): # pylint: disable=duplicate-bases
    """Don't fail when the MRO is invalid."""
    def test(self):
        super().lalala()

type(Client()).ala # [no-member]
type({}).bala # [no-member]
type('').portocala # [no-member]


def socket_false_positive():
    """Test a regression
    Version used:

    - Pylint 0.10.0
    - Logilab common 0.15.0
    - Logilab astroid 0.15.1

    False E1101 positive, line 23:
    Instance of '_socketobject' has no 'connect' member
    """

    import socket
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(('127.0.0.1', 80))
    sckt.close()


def no_conjugate_member(magic_flag):
    """should not raise E1101 on something.conjugate"""
    if magic_flag:
        something = 1.0
    else:
        something = 1.0j
    if isinstance(something, float):
        return something
    return something.conjugate()


class NoDunderNameInInstance(object):
    """Emit a warning when accessing __name__ from an instance."""
    def __init__(self):
        self.var = self.__name__ # [no-member]


class InvalidAccessBySlots(object):
    __slots__ = ('a', )
    def __init__(self):
        var = self.teta # [no-member]
        self.teta = 24


class MetaWithDynamicGetattr(type):

    def __getattr__(cls, attr):
        return attr


class SomeClass(object, metaclass=MetaWithDynamicGetattr):
    pass


SomeClass.does_not_exist

class ClassWithMangledAttribute(object):
    def __init__(self):
        self.name = 'Bug1643'
    def __bar(self):
        print(self.name + "xD")

ClassWithMangledAttribute()._ClassWithMangledAttribute__bar()  # pylint: disable=protected-access


import enum


class Cls(enum.IntEnum):
    BAR = 0


SOME_VALUE = Cls.BAZ  # [no-member]



# Does not crash when inferring the `append` attribute on the slice object
class SomeClassUsingSlice:
    def __init__(self, flag):
        if flag:
            self.attribute = slice(None)
        else:
            self.attribute = []
            self.attribute.append(1)

from enum import Enum
class Animal(Enum):
    ANT = 1
    BEE = 2
    CAT = 3
    DOG = 4
# To test false positive no-member on Enum.__members__.items()
for itm in Animal.__members__.items():
    print(itm)
for keyy in Animal.__members__.keys():  # pylint: disable=consider-iterating-dictionary
    print(keyy)
for vall in Animal.__members__.values():
    print(vall)
