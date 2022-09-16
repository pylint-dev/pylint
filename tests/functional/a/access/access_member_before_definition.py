# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
# pylint: disable=attribute-defined-outside-init


class Aaaa:
    """class with attributes defined in wrong order"""

    def __init__(self):
        var1 = self._var2  # [access-member-before-definition]
        self._var2 = 3
        self._var3 = var1


class Bbbb:
    A = 23
    B = A

    def __getattr__(self, attr):
        try:
            return self.__repo
        except AttributeError:
            self.__repo = attr
            return attr

    def catchme(self, attr):
        """no AttributeError caught"""
        try:
            return self._repo  # [access-member-before-definition]
        except ValueError:
            self._repo = attr
            return attr


class Mixin:
    def test_mixin(self):
        """Don't emit access-member-before-definition for mixin classes."""
        if self.already_defined:
            # pylint: disable=attribute-defined-outside-init
            self.already_defined = None


# Test for regression in bitbucket issue 164
# https://bitbucket.org/logilab/pylint/issue/164/
class MyClass1:
    def __init__(self):
        self.first += 5  # [access-member-before-definition]
        self.first = 0
