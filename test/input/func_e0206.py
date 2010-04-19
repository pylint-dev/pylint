# pylint: disable=R0903
"""check for interface which are not classes"""

__revision__ = None

class Abcd:
    """dummy"""
    __implements__ = __revision__
    
    def __init__(self):
        self.attr = None 

class Cdef:
    """dummy"""
    __implements__ = (__revision__, Abcd)

    def __init__(self):
        pass


