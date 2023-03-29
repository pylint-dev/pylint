# pylint: disable=too-few-public-methods,import-error, missing-docstring
# pylint: disable=useless-super-delegation,wrong-import-position,invalid-name, wrong-import-order
# pylint: disable=super-with-arguments
from unknown import Missing

class Aaaa:
    """old style"""
    def hop(self):
        """hop"""
        super(Aaaa, self).hop() # >=3.0:[no-member]

    def __init__(self):
        super(Aaaa, self).__init__()

class NewAaaa:
    """old style"""
    def hop(self):
        """hop"""
        super(NewAaaa, self).hop() # [no-member]

    def __init__(self):
        super(Aaaa, self).__init__()  # [bad-super-call]

class Py3kAaaa(NewAaaa):
    """new style"""
    def __init__(self):
        super().__init__()  # <3.0:[missing-super-argument]

class Py3kWrongSuper(Py3kAaaa):
    """new style"""
    def __init__(self):
        super(NewAaaa, self).__init__()

class WrongNameRegression(Py3kAaaa):
    """ test a regression with the message """
    def __init__(self):
        super(Missing, self).__init__()  # [bad-super-call]

class Getattr:
    """ crash """
    name = NewAaaa

class CrashSuper:
    """ test a crash with this checker """
    def __init__(self):
        super(Getattr.name, self).__init__()  # [bad-super-call]

class Empty:
    """Just an empty class."""

class SuperDifferentScope:
    """Don'emit bad-super-call when the super call is in another scope.
    For reference, see https://bitbucket.org/logilab/pylint/issue/403.
    """
    @staticmethod
    def test():
        """Test that a bad-super-call is not emitted for this case."""
        class FalsePositive(Empty):
            """The following super is in another scope than `test`."""
            def __init__(self, arg):
                super(FalsePositive, self).__init__(arg)
        super(object, 1).__init__()


class UnknownBases(Missing):
    """Don't emit if we don't know all the bases."""
    def __init__(self):
        super(UnknownBases, self).__init__()
        super(UnknownBases, self).test()
        super(Missing, self).test() # [bad-super-call]


# Test that we are detecting proper super errors.

class BaseClass:

    not_a_method = 42

    def function(self, param):
        return param + self.not_a_method

    def __getattr__(self, attr):
        return attr


class InvalidSuperChecks(BaseClass):

    def __init__(self):
        super(InvalidSuperChecks, self).not_a_method() # [not-callable]
        super(InvalidSuperChecks, self).attribute_error() # [no-member]
        super(InvalidSuperChecks, self).function(42)
        super(InvalidSuperChecks, self).function() # [no-value-for-parameter]
        super(InvalidSuperChecks, self).function(42, 24, 24) # [too-many-function-args]
        # +1: [unexpected-keyword-arg,no-value-for-parameter]
        super(InvalidSuperChecks, self).function(lala=42)
        # Even though BaseClass has a __getattr__, that won't
        # be called.
        super(InvalidSuperChecks, self).attribute_error() # [no-member]



# Regression for pylint-dev/pylint/issues/773
import subprocess

# The problem was related to astroid not filtering statements
# at scope level properly, basically not doing strong updates.
try:
    TimeoutExpired = subprocess.TimeoutExpired
except AttributeError:
    class TimeoutExpired(subprocess.CalledProcessError):
        def __init__(self):
            returncode = -1
            self.timeout = -1
            super(TimeoutExpired, self).__init__("", returncode)


class SuperWithType:
    """type(self) may lead to recursion loop in derived classes"""
    def __init__(self):
        super(type(self), self).__init__() # [bad-super-call]

class SuperWithSelfClass:
    """self.__class__ may lead to recursion loop in derived classes"""
    def __init__(self):
        super(self.__class__, self).__init__() # [bad-super-call]


# Reported in https://github.com/pylint-dev/pylint/issues/2903
class Parent:
    def method(self):
        print()


class Child(Parent):
    def method(self):
        print("Child")
        super().method()

class Niece(Parent):
    def method(self):
        print("Niece")
        super().method()

class GrandChild(Child):
    def method(self):
        print("Grandchild")
        super(GrandChild, self).method()
        super(Child, self).method()
        super(Niece, self).method()  # [bad-super-call]


# Reported in https://github.com/pylint-dev/pylint/issues/4922
class AlabamaCousin(Child, Niece):
    def method(self):
        print("AlabamaCousin")
        super(Child, self).method()
