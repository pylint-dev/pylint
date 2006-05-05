# pylint: disable-msg=R0903,W0212
"""test for call to __init__ from a non ancestor class
"""

__revision__ = '$Id: func_w0233.py,v 1.2 2004-09-29 08:35:13 syt Exp $'

class AAAA:
    """ancestor 1"""

    def __init__(self):
        print 'init', self
        BBBB.__init__(self)

class BBBB:
    """ancestor 2"""

    def __init__(self):
        print 'init', self
        
