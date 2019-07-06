# pylint: disable=R0903,import-error,missing-docstring,wrong-import-position,useless-super-delegation, useless-object-inheritance, unnecessary-pass
"""test for __init__ not called
"""
from __future__ import print_function

class AAAA:
    """ancestor 1"""

    def __init__(self):
        print('init', self)

class BBBB:
    """ancestor 2"""

    def __init__(self):
        print('init', self)

class CCCC:
    """ancestor 3"""


class ZZZZ(AAAA, BBBB, CCCC):
    """derived class"""

    def __init__(self):  # [super-init-not-called]
        AAAA.__init__(self)

class NewStyleA(object):
    """new style class"""
    def __init__(self):
        super(NewStyleA, self).__init__()
        print('init', self)

class NewStyleB(NewStyleA):
    """derived new style class"""
    def __init__(self):
        super(NewStyleB, self).__init__()

class NoInit(object):
    """No __init__ defined"""

class Init(NoInit):
    """Don't complain for not calling the super __init__"""

    def __init__(self, arg):
        self.arg = arg

class NewStyleC(object):
    """__init__ defined by assignment."""
    def xx_init(self):
        """Initializer."""
        pass

    __init__ = xx_init

class AssignedInit(NewStyleC):
    """No init called."""
    def __init__(self):  # [super-init-not-called]
        self.arg = 0

from missing import Missing

class UnknownBases(Missing):
    """Don't emit no-init if the bases aren't known."""
