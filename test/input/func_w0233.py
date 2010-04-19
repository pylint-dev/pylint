# pylint: disable=R0903,W0212,W0403,W0406
"""test for call to __init__ from a non ancestor class
"""

__revision__ = '$Id: func_w0233.py,v 1.2 2004-09-29 08:35:13 syt Exp $'

class AAAA:
    """ancestor 1"""

    def __init__(self):
        print 'init', self
        BBBBMixin.__init__(self)

class BBBBMixin:
    """ancestor 2"""

    def __init__(self):
        print 'init', self

import nonexistant
import func_w0233
class CCC(BBBBMixin, func_w0233.AAAA, func_w0233.BBBB, nonexistant.AClass):
    """mix different things, some inferable some not"""
    def __init__(self):
        BBBBMixin.__init__(self)
        func_w0233.AAAA.__init__(self)
        func_w0233.BBBB.__init__(self)
        nonexistant.AClass.__init__(self)

class DDDD(AAAA):
    """call superclass constructor in disjunct branches"""
    def __init__(self, value):
        if value:
            AAAA.__init__(self)
        else:
            AAAA.__init__(self)
