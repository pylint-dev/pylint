"""Checks classes methods are declared with a decorator if whithin the class
scope and if classmethod's argument is a member of the class
"""

# pylint: disable=too-few-public-methods

class MyClass(object):
    """Some class"""
    def __init__(self):
        pass

    def cmethod(cls):
        """class method-to-be"""
    cmethod = classmethod(cmethod) # [no-classmethod-decorator]

    @classmethod
    def my_second_method(cls):
        """correct class method definition"""

def helloworld():
    """says hello"""
    print 'hello world'

MyClass.new_class_method = classmethod(helloworld)

class MyOtherClass(object):
    """Some other class"""
    _make = classmethod(tuple.__new__)
