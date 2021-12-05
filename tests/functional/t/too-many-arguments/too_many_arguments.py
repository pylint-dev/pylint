# pylint: disable=missing-docstring,wrong-import-position

def stupid_function(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9): # [too-many-arguments]
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
    """Test we don't emit a FP for https://github.com/PyCQA/pylint/issues/2588"""
    partial_func = partial(root_function, 1, 2, 3)
    partial_func()
    return root_function(1, 2, 3)
