"""Class statements whose base is an instance build an instance of the type of that
base, like ``zope.interface`` interfaces. When that type is not a subclass of ``type``
the result is not a class, so the functions defined in its body are not methods.
"""

# pylint: disable=import-error, missing-docstring, too-few-public-methods
# pylint: disable=unused-argument, invalid-name

from missing import Missing


class InterfaceClass:
    """Mimic ``zope.interface.interface.InterfaceClass``."""

    def __init__(self, name, bases=(), attrs=None, doc=None, module=None):
        self.name = name

    def __str__(self):
        return self.name


Interface = InterfaceClass("Interface")


class IThing(Interface):
    def __str__():
        """Not a method, the class statement does not create a class."""

    def method(arg):
        """Not a method either."""


class ISubThing(IThing):
    def method(arg, other):
        """Sub-interfaces don't create classes either."""


class Ancestor:
    pass


class Parent(Ancestor):
    pass


class Child(Parent):  # [too-many-ancestors]
    pass


class VarArgs:
    def __init__(self, *args):
        self.args = args


class IVarArgs(VarArgs()):
    def method():
        """Not a method."""


class TooFewArgs:
    def __init__(self, name):
        self.name = name


class Bad(TooFewArgs("name")):  # [inherit-non-class]
    def method():  # [no-method-argument]
        """Calling 'TooFewArgs' with the class statement arguments fails."""


class TooManyArgs:
    def __init__(self, name, bases, namespace, other):
        self.name = name


class Bad1(TooManyArgs(1, 2, 3, 4)):  # [inherit-non-class]
    def method():  # [no-method-argument]
        """Calling 'TooManyArgs' with the class statement arguments fails."""


class RequiredKeywordOnly:
    def __init__(self, name, bases, namespace, *, other):
        self.name = name


class Bad2(RequiredKeywordOnly(1, 2, 3, other=4)):  # [inherit-non-class]
    def method():  # [no-method-argument]
        """Calling 'RequiredKeywordOnly' with the class statement arguments fails."""


class MroEntries:
    def __init__(self, name, bases, namespace):
        self.name = name

    def __mro_entries__(self, bases):
        return (object,)


class WithMroEntries(MroEntries(1, 2, 3)):  # [inherit-non-class]
    def method():  # [no-method-argument]
        """'__mro_entries__' replaces the base, so this is a class."""


def _init(self, name, bases, namespace):
    self.name = name


class AssignedInit:
    __init__ = _init


class Unknown(AssignedInit(1, 2, 3)):  # [inherit-non-class]
    def method():  # [no-method-argument]
        """The constructor of 'AssignedInit' is not inferred."""


class UnknownBase(Missing):
    pass


class Unknown1(UnknownBase()):  # [inherit-non-class]
    def method():  # [no-method-argument]
        """The constructor of 'UnknownBase' is not found."""
