# pylint: disable=missing-docstring

def stupid_function(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9): # [too-many-arguments]
    return arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9


class MyClass:
    text = "MyText"

    def mymethod1(self):
        return self.text

    def mymethod2(self):
        return self.mymethod1.__get__(self, MyClass)


MyClass().mymethod2()()
