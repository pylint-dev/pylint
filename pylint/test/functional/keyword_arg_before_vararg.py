"""Unittests for W1125 (kw args before *args)"""
from __future__ import absolute_import, print_function

# pylint: disable=unused-argument, useless-object-inheritance
def check_kwargs_before_args(param1, param2=2, *args): # [keyword-arg-before-vararg]
    """docstring"""
    pass

check_kwargs_before_args(5)

# pylint: disable=too-few-public-methods, invalid-name
class AAAA(object):
    """class AAAA"""
    def func_in_class(self, param1, param2=2, *args): # [keyword-arg-before-vararg]
        "method in class AAAA"
        pass

    @staticmethod
    def static_method_in_class(param1, param2=3, *args): # [keyword-arg-before-vararg]
        "static method in class AAAA"
        pass

    @classmethod
    def class_method_in_class(cls, param1, param2=4, *args): # [keyword-arg-before-vararg]
        "class method in class AAAA"
        pass

some_var = AAAA()
some_var.func_in_class(3)

some_var.static_method_in_class(4)
AAAA.static_method_in_class(4)

some_var.class_method_in_class(5)
AAAA.class_method_in_class(5)
