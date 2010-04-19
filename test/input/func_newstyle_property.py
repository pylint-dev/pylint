# pylint: disable=R0903
"""test property on old style class"""

__revision__ = 1

def getter(self):
    """interesting"""
    return self

class OkOk(object):
    """correct usage"""
    method = property(getter, doc='hop')
    
class HaNonNonNon:
    """bad usage"""
    method = property(getter, doc='hop')
    
    def __init__(self):
        pass
