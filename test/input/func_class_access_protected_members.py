# pylint: disable=R0903
"""test external access to protected class members"""

__revision__ = ''

class MyClass:
    """class docstring"""
    _cls_protected = 5
    
    def __init__(self, other):
        """init"""
        self._protected = 1
        self.public = other
        
        
    def test(self):
        """test"""
        self._protected += self._cls_protected
        print self.public._haha
        
    def clsmeth(cls):
        """this is ok"""
        print cls._cls_protected
    clsmeth = classmethod(clsmeth)
    
INST = MyClass()
print INST.public
print INST._protected
print INST._cls_protected

