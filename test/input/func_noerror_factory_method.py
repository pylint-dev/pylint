# pylint: disable=R0903
"""use new astng context sensitive inference"""
__revision__ = 1

class Super(object):
    """super class"""
    def __init__(self):
        self.bla = None
        
    def instance(cls):
        """factory method"""
        return cls()
    instance = classmethod(instance)
    
class Sub(Super):
    """dub class"""
    def method(self):
        """specific method"""
        print 'method called', self

# should see the Sub.instance() is returning a Sub instance, not a Super
# instance
Sub.instance().method()
