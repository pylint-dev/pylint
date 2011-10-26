# pylint: disable=R0903
"""test property on old style class and property.setter/deleter usage"""

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

class SomeClass(object):
    """another docstring"""

    def __init__(self):
        self._prop = None

    @property
    def prop(self):
        """I'm the 'prop' property."""
        return self._prop

    @prop.setter
    def prop(self, value):
        """I'm the 'prop' property."""
        self._prop = value

    @prop.deleter
    def prop(self):
        """I'm the 'prop' property."""
        del self._prop
