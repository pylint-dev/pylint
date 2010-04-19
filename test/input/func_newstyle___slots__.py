# pylint: disable=R0903
"""test __slots__ on old style class"""

__revision__ = 1

class OkOk(object):
    """correct usage"""
    __slots__ = ('a', 'b')
    
class HaNonNonNon:
    """bad usage"""
    __slots__ = ('a', 'b')

    def __init__(self):
        pass

__slots__ = 'hop' # pfff
