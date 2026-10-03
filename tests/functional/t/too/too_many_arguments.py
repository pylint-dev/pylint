# pylint: disable=missing-docstring,wrong-import-position,unnecessary-dunder-call

# +1: [too-many-arguments, too-many-positional-arguments]
def stupid_function(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9):
    return arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9


class MyClass:
    text = "MyText"

    def mymethod1(self):
        return self.text

    def mymethod2(self):
        return self.mymethod1.__get__(self, MyClass)


MyClass().mymethod2()()


# Check a false positive does not occur
from functools import partial


def root_function(first, second, third):
    return first + second + third


def func_call():
    """Test we don't emit a FP for https://github.com/pylint-dev/pylint/issues/2588"""
    partial_func = partial(root_function, 1, 2, 3)
    partial_func()
    return root_function(1, 2, 3)


# +1: [too-many-arguments]
def name1(param1, param2, param3, /, param4, param5, *args, param6="apple", **kwargs):
    return param1, param2, param3, param4, param5, param6, args, kwargs
