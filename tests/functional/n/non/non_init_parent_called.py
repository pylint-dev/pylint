# pylint: disable=protected-access,import-self,too-few-public-methods,line-too-long
# pylint: disable=wrong-import-order, unnecessary-dunder-call
"""test for call to __init__ from a non ancestor class
"""
from . import non_init_parent_called
import nonexistent  # [import-error]


class AAAA:
    """ancestor 1"""

    def __init__(self):
        print('init', self)
        BBBBMixin.__init__(self)  # [non-parent-init-called]

class BBBBMixin:
    """ancestor 2"""

    def __init__(self):
        print('init', self)

class CCC(BBBBMixin, non_init_parent_called.AAAA, non_init_parent_called.BBBB, nonexistent.AClass):  # [no-member]
    """mix different things, some inferable some not"""
    def __init__(self):
        BBBBMixin.__init__(self)
        non_init_parent_called.AAAA.__init__(self)
        non_init_parent_called.BBBB.__init__(self)  # [no-member]
        nonexistent.AClass.__init__(self)

class DDDD(AAAA):
    """call superclass constructor in disjunct branches"""
    def __init__(self, value):
        if value:
            AAAA.__init__(self)
        else:
            AAAA.__init__(self)

class Super(dict):
    """ test late binding super() call """
    def __init__(self):
        base = super()
        base.__init__()

class Super2(dict):
    """ Using the same idiom as Super, but without calling
    the __init__ method.
    """
    def __init__(self):
        base = super()
        base.__woohoo__()  # [no-member]
