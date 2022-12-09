# pylint: disable=invalid-name,too-many-public-methods,attribute-defined-outside-init
# pylint: disable=too-few-public-methods,deprecated-module
"""This module demonstrates a possible problem of pyLint with calling __init__ s
from inherited classes.
Initializations done there are not considered, which results in Error E0203 for
self.cookedq."""


class Tomato:
    """The base Tomato class"""
    def __init__(self, juicy_index=42, deliciousness=100):
        self.juicy_index = juicy_index
        self.deliciousness = deliciousness

    def print_description(self, label="generic"):
        print(f"{label} tomato")


class GreenTomato(Tomato):
    """Extension of Tomato"""

    def __init__(self, juicy_index=0, deliciousness=0):
        Tomato.__init__(self, juicy_index, deliciousness)

    def print_me(self):
        """print a desciption"""
        self.print_description("green")


class Base:
    """bla bla"""
    dougloup_papa = None

    def __init__(self):
        self._var = False

class Derived(Base):
    """derived blabla"""
    dougloup_moi = None
    def Work(self):
        """do something"""
        # E0203 - Access to member '_var' before its definition
        if self._var:
            print("True")
        else:
            print("False")
        self._var = True

        # E0203 - Access to member 'dougloup_papa' before its definition
        if self.dougloup_papa:
            print('dougloup !')
        self.dougloup_papa = True
        # E0203 - Access to member 'dougloup_moi' before its definition
        if self.dougloup_moi:
            print('dougloup !')
        self.dougloup_moi = True


class QoSALConnection:
    """blabla"""

    _the_instance = None

    def __new__(cls):
        if cls._the_instance is None:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def __init__(self):
        pass

class DefinedOutsideInit:
    """use_attr is seen as the method defining attr because its in
    first position
    """
    def __init__(self):
        self.reset()

    def use_attr(self):
        """use and set members"""
        if self.attr:
            print('hop')
        self.attr = 10

    def reset(self):
        """reset members"""
        self.attr = 4
