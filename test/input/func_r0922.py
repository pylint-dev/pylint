"""test max methods"""
__revision__ = None

class Aaaa:
    """yo"""
    def __init__(self):
        pass
    
    def meth1(self):
        """hehehe"""
        raise NotImplementedError
    
    def meth2(self):
        """hehehe"""
        return 'Yo', self

class Bbbb(Aaaa):
    """yeah"""
    def meth1(self):
        """hehehe bis"""
        return "yeah", self
