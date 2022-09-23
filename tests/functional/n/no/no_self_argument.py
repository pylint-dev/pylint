"""Check for method without self as first argument"""


MYSTATICMETHOD = staticmethod


def returns_staticmethod(my_function):
    """Create a staticmethod from function `my_function`"""
    return staticmethod(my_function)


class NoSelfArgument:
    """dummy class"""

    def __init__(truc):  # [no-self-argument]
        """method without self"""
        print(1)

    def abdc(yoo):  # [no-self-argument]
        """another test"""
        print(yoo)

    def edf(self):
        """just another method"""
        print('yapudju in', self)

    @staticmethod
    def say_hello():
        """A standard staticmethod"""
        print("hello!")

    @MYSTATICMETHOD
    def say_goodbye():
        """A staticmethod but using a different name"""
        print("goodbye!")

    @returns_staticmethod
    def concatenate_strings(string1, string2):
        """A staticmethod created by `returns_staticmethod` function"""
        return string1 + string2

    def varargs(*args):  # [no-self-argument]
        """A method without a self argument but with *args."""

    def kwargs(**kwargs):  # [no-self-argument]
        """A method without a self argument but with **kwargs."""

    def varargs_and_kwargs(*args, **kwargs):  # [no-self-argument]
        """A method without a self argument but with *args and **kwargs."""
