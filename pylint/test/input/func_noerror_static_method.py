"""Checks if static / class methods works fine in Pylint
"""
from __future__ import print_function
__revision__ = ''

#pylint: disable=no-classmethod-decorator, no-staticmethod-decorator
class MyClass(object):
    """doc
    """
    def __init__(self):
        pass

    def static_met(var1, var2):
        """This is a static method
        """
        print(var1, var2)

    def class_met(cls, var1):
        """This is a class method
        """
        print(cls, var1)

    static_met = staticmethod(static_met)
    class_met = classmethod(class_met)

if __name__ == '__main__':
    MyClass.static_met("var1", "var2")
    MyClass.class_met("var1")
