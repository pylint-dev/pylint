# pylint: disable=R0903
"""test for __init__ not called
"""

__revision__ = '$Id: func_w0231.py,v 1.3 2004-09-29 08:35:13 syt Exp $'

class AAAA:
    """ancestor 1"""

    def __init__(self):
        print 'init', self

class BBBB:
    """ancestor 2"""

    def __init__(self):
        print 'init', self

class CCCC:
    """ancestor 3"""


class ZZZZ(AAAA, BBBB, CCCC):
    """derived class"""

    def __init__(self):
        AAAA.__init__(self)

class NewStyleA(object):
    """new style class"""
    def __init__(self):
        super(NewStyleA, self).__init__()
        print 'init', self

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
    """__init__ defined by assignemnt."""
    def xx_init(self):
        """Initializer."""
        pass

    __init__ = xx_init

class AssignedInit(NewStyleC):
    """No init called."""
    def __init__(self):
        self.arg = 0
