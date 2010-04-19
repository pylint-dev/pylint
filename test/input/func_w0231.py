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
