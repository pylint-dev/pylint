"""Checks static methods are declared with a decorator if whithin the class
scope and if static method's argument is a member of the class
"""

# pylint: disable=too-few-public-methods

class MyClass(object):
    """Some class"""
    def __init__(self):
        pass

    def smethod():
        """static method-to-be"""
    smethod = staticmethod(smethod) # [no-staticmethod-decorator]

    @staticmethod
    def my_second_method():
        """correct static method definition"""

def helloworld():
    """says hello"""
    print 'hello world'

MyClass.new_static_method = staticmethod(helloworld)

class MyOtherClass(object):
    """Some other class"""
    _make = staticmethod(tuple.__new__)
