# pylint: disable=R0903,R0922
"""test overriding of abstract method
"""

__revision__ = '$Id: func_w0223.py,v 1.2 2004-09-29 08:35:13 syt Exp $'

class Abstract:
    """abstract class
    """
    def aaaa(self):
        """should be overridden in concrete class"""
        raise NotImplementedError()


    def bbbb(self):
        """should be overridden in concrete class"""
        raise NotImplementedError()

    def __init__(self):
        pass

class AbstractB(Abstract):
    """abstract class
    this class is checking that it does not output an error msg for
    unimplemeted methods in abstract classes
    """
    def cccc(self):
        """should be overridden in concrete class"""
        raise NotImplementedError()

class Concret(Abstract):
    """concret class"""

    def aaaa(self):
        """overidden form Abstract"""
        print self
