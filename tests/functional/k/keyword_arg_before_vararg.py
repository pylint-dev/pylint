"""Unittests for W1125 (kw args before *args)"""

# pylint: disable=missing-function-docstring, unused-argument, unnecessary-pass
def check_kwargs_before_args(param1, param2=2, *args): # [keyword-arg-before-vararg]
    """docstring"""
    pass

check_kwargs_before_args(5)

# pylint: disable=too-few-public-methods, invalid-name
class AAAA:
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


def name1(param1, /, param2=True, *args): ...  # [keyword-arg-before-vararg]
def name2(param1=True, /, param2=True, *args): ...  # [keyword-arg-before-vararg]
def name3(param1, param2=True, /, param3=True, *args): ...  # [keyword-arg-before-vararg]
def name4(param1, /, *args): ...
def name5(param1=True, /, *args): ...
def name6(param1, /, *args, param2=True): ...
def name7(param1=True, /, *args, param2=True): ...
def name8(param1, param2=True, /, *args, param3=True): ...
