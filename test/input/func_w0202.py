"""check static method with self or cls as first argument"""

__revision__ = None

class Abcd:
    """dummy"""
    
    def method1(self):
        """hehe"""
    method1 = staticmethod(method1)

    def method2(cls):
        """hehe"""
    method2 = staticmethod(method2)

    def __init__(self):
        pass
