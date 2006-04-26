"""test max methods"""
__revision__ = None

from logilab.common.interface import Interface

class IAaaa(Interface):
    """yo"""
    
    def meth1(self):
        """hehehe"""
        
class IBbbb(Interface):
    """yo"""
    
    def meth1(self):
        """hehehe"""

class Concret:
    """implements IBbbb"""
    __implements__ = IBbbb

    def __init__(self):
        pass
    
    def meth1(self):
        """hehehe"""
        return "et hop", self
    
    def meth2(self):
        """hehehe"""
        return "et hop", self
    
