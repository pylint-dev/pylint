"""Unittests for W1125 (kw args before *args)"""
from __future__ import absolute_import, print_function

# pylint: disable=unused-argument
def check_kwargs_before_args(param1, param2=2, *args):
    """docstring"""
    pass

check_kwargs_before_args(5) # [keyword-arg-before-vararg]

# pylint: disable=too-few-public-methods, invalid-name
class AAAA(object):
    """class AAAA"""
    def func_in_class(self, param1, param2=2, *args):
        "method in class AAAA"
        pass

    @staticmethod
    def static_method_in_class(param1, param2=3, *args):
        "static method in class AAAA"
        pass

    @classmethod
    def class_method_in_class(cls, param1, param2=4, *args):
        "class method in class AAAA"
        pass

some_var = AAAA()
some_var.func_in_class(3) # [keyword-arg-before-vararg]

some_var.static_method_in_class(4) # [keyword-arg-before-vararg]
AAAA.static_method_in_class(4) # [keyword-arg-before-vararg]

some_var.class_method_in_class(5) # [keyword-arg-before-vararg]
AAAA.class_method_in_class(5) # [keyword-arg-before-vararg]
