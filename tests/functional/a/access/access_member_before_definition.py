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


class BareAnnotationNotADefinition:
    def process(self):
        _ = self.widget  # known false negative
        self.widget: int


class AnnotatedAssignmentIsADefinition:
    def process(self):
        _ = self.widget  # [access-member-before-definition]
        self.widget: int = 5


class AccessInCalledMethod:
    def __init__(self, other):
        str()
        other.use_later()

        def nested():
            self.use_later()

        self.use_later()  # [access-member-before-definition]
        self.later = 1
        nested()

    def use_later(self):
        return self.later


class DefinedBeforeCalledMethod:
    def __init__(self):
        self.defined = 1
        self.use_defined()

    def use_defined(self):
        return self.defined


class AccessInLambda:
    def __init__(self):
        self.callback = lambda: self.later
        self.later = 1
