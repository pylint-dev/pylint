"""Checks that class variables are seen as inherited !
"""

__revision__ = ''


class MyClass:
    """Inherits from nothing 
    """

    def __init__(self):
        self.var = {}

    def met(self):
        """Checks that base_var is seen as defined outside '__init__'
        """
        self.var[1] = 'one'
        self.base_var = 'one'
        print self.base_var, self.var

    def met2(self):
        """dummy method"""
        print self
class MySubClass(MyClass):
    """Inherits from MyClass
    """
    class_attr = 1
    
    def __init__(self):
        MyClass.__init__(self)
        self.var2 = 2
        print self.__doc__
        print self.__dict__
        print self.__class__

    def met2(self):
        """Checks that var is seen as defined outside '__init__'
        """
        self.var[1] = 'one'
        self.var2 += 1
        print self.class_attr
        
if __name__ == '__main__':
    OBJ = MyClass()
    OBJ.met()

