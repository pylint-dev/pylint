# pylint: disable-msg=R0903
"""test unused argument
"""

__revision__ = 1

def function(arg=1):
    """ignore arg"""


class AAAA:
    """dummy class"""

    def method(self, arg):
        """dummy method"""
        print self
    def __init__(self):
        pass

    @classmethod
    def selected(cls, *args, **kwargs):
        """called by the registry when the vobject has been selected.
        """
        return cls
