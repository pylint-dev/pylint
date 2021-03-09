"""Test detection of self as argument of first method in Python 3.7 and above."""

# pylint: disable=missing-docstring,too-few-public-methods,useless-object-inheritance


class Toto(object):

    def __class_getitem__(cls, params):
        # This is actually a special method which is always a class method.
        # See https://www.python.org/dev/peps/pep-0560/#class-getitem
        pass

    def __class_other__(cls, params):  # [no-self-argument]
        # This is not a special case and as such is an instance method.
        pass
