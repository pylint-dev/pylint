# pylint: disable=too-few-public-methods, import-error, missing-docstring, wrong-import-position
# pylint: disable=useless-super-delegation, useless-object-inheritance, unnecessary-pass

from __future__ import print_function

from typing import overload

from missing import Missing


class AAAA:
    """ancestor 1"""

    def __init__(self):
        print("init", self)


class BBBB:
    """ancestor 2"""

    def __init__(self):
        print("init", self)


class CCCC:
    """ancestor 3"""


class ZZZZ(AAAA, BBBB, CCCC):
    """derived class"""

    def __init__(self):  # [super-init-not-called]
        AAAA.__init__(self)


class NewStyleA(object):
    """new style class"""

    def __init__(self):
        super().__init__()
        print("init", self)


class NewStyleB(NewStyleA):
    """derived new style class"""

    def __init__(self):
        super().__init__()


class NewStyleC(object):
    """__init__ defined by assignment."""

    def xx_init(self):
        """Initializer."""
        pass

    __init__ = xx_init


class AssignedInit(NewStyleC):
    """No init called, but abstract so that is fine."""

    def __init__(self):
        self.arg = 0


class UnknownBases(Missing):
    """No false positives if the bases aren't known."""


class Parent:
    def __init__(self, num: int):
        self.number = num


class Child(Parent):
    @overload
    def __init__(self, num: int):
        ...

    @overload
    def __init__(self, num: float):
        ...

    def __init__(self, num):
        super().__init__(round(num))
