"""Check if a class inherits from object.
In python3 every class implicitly inherits from object, therefore give refactoring message to
 remove object from bases"""
# pylint: disable=no-init, invalid-name, missing-docstring, too-few-public-methods
# pylint: disable=inconsistent-mro
import abc

class A(object):    # [useless-object-inheritance]
    pass

class B:
    pass

class C(B, object): # [useless-object-inheritance]
    pass

class D(object, C, metaclass=abc.ABCMeta):   # [useless-object-inheritance]
    pass

class E(D, C, object, metaclass=abc.ABCMeta):   # [useless-object-inheritance]
    pass

class F(A): # positive test case
    pass

class G(B): # positive test case
    pass
