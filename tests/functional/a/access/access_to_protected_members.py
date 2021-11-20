# pylint: disable=too-few-public-methods, super-init-not-called
# pylint: disable=no-classmethod-decorator,useless-object-inheritance
"""Test external access to protected class members."""
from __future__ import print_function

class MyClass(object):
    """Class with protected members."""
    _cls_protected = 5

    def __init__(self, other):
        MyClass._cls_protected = 6
        self._protected = 1
        self.public = other
        self.attr = 0

    def test(self):
        """Docstring."""
        self._protected += self._cls_protected
        print(self.public._haha)  # [protected-access]

    def clsmeth(cls):
        """Docstring."""
        cls._cls_protected += 1
        print(cls._cls_protected)
    clsmeth = classmethod(clsmeth)

    def _private_method(self):
        """Doing nothing."""


class Subclass(MyClass):
    """Subclass with protected members."""

    def __init__(self):
        MyClass._protected = 5
        super()._private_method()

INST = Subclass()
INST.attr = 1
print(INST.attr)
INST._protected = 2  # [protected-access]
print(INST._protected)  # [protected-access]
INST._cls_protected = 3  # [protected-access]
print(INST._cls_protected)  # [protected-access]


class Issue1031(object):
    """Test for GitHub issue 1031"""
    _attr = 1

    def correct_access(self):
        """Demonstrates correct access"""
        return type(self)._attr

    def incorrect_access(self):
        """Demonstrates incorrect access"""
        if self._attr == 1:
            return type(INST)._protected  # [protected-access]
        return None


class Issue1802(object):
    """Test for GitHub issue 1802"""
    def __init__(self, value):
        self._foo = value
        self.__private = 2 * value

    def __eq__(self, other):
        """Test a correct access as the access to protected member is in a special method"""
        if isinstance(other, self.__class__):
            answer = self._foo == other._foo
            return answer and self.__private == other.__private  # [protected-access]
        return False

    def not_in_special(self, other):
        """
        Test an incorrect access as the access to protected member is not inside a special method
        """
        if isinstance(other, self.__class__):
            return self._foo == other._foo  # [protected-access]
        return False

    def __le__(self, other):
        """
        Test a correct access as the access to protected member
        is inside a special method even if it is deeply nested
        """
        if 2 > 1:
            if isinstance(other, self.__class__):
                if "answer" == "42":
                    return self._foo == other._foo
        return False

    def __fake_special__(self, other):
        """
        Test an incorrect access as the access
        to protected member is not inside a licit special method
        """
        if isinstance(other, self.__class__):
            return self._foo == other._foo  # [protected-access]
        return False


class Issue1159OtherClass(object):
    """Test for GitHub issue 1159"""

    _foo = 0

    def __init__(self):
        self._bar = 0


class Issue1159(object):
    """Test for GitHub issue 1159"""

    _foo = 0

    def __init__(self):
        self._bar = 0

    @classmethod
    def access_cls_attr(cls):
        """
        Access to protected class members inside class methods is OK.
        """

        _ = cls._foo

    @classmethod
    def assign_cls_attr(cls):
        """
        Assignment to protected class members inside class methods is OK.
        """

        cls._foo = 1

    @classmethod
    def access_inst_attr(cls):
        """
        Access to protected instance members inside class methods is OK.
        """

        instance = cls()
        _ = instance._bar

    @classmethod
    def assign_inst_attr(cls):
        """
        Assignment to protected members inside class methods is OK.
        """

        instance = cls()
        instance._bar = 1

    @classmethod
    def access_other_attr(cls):
        """
        Access to protected instance members of other classes is not OK.
        """

        instance = Issue1159OtherClass()
        instance._bar = 3  # [protected-access]
        _ = instance._foo  # [protected-access]


class Issue1159Subclass(Issue1159):
    """Test for GitHub issue 1159"""

    @classmethod
    def access_inst_attr(cls):
        """
        Access to protected instance members inside class methods is OK.
        """

        instance = cls()
        _ = instance._bar

    @classmethod
    def assign_inst_attr(cls):
        """
        Assignment to protected instance members inside class methods is OK.
        """

        instance = cls()
        instance._bar = 1

    @classmethod
    def access_missing_member(cls):
        """
        Access to unassigned members inside class methods is not OK.
        """

        instance = cls()
        _ = instance._baz  # [no-member,protected-access]

    @classmethod
    def assign_missing_member(cls):
        """
        Defining attributes outside init is still not OK.
        """

        instance = cls()
        instance._qux = 1  # [attribute-defined-outside-init]

    @classmethod
    def access_other_attr(cls):
        """
        Access to protected instance members of other classes is not OK.
        """

        instance = Issue1159OtherClass()
        instance._bar = 3  # [protected-access]
        _ = instance._foo  # [protected-access]


class Issue3066:
    """Test for GitHub issue 3066
    Accessing of attributes/methods of inner and outer classes
    https://github.com/PyCQA/pylint/issues/3066"""

    attr = 0
    _attr = 1

    @staticmethod
    def _bar(i):
        """Docstring."""

    @staticmethod
    def foobar(i):
        """Test access from outer class"""
        Issue3066._attr = 2
        Issue3066.Aclass._attr = "y"  # [protected-access]
        Issue3066.Aclass.Bclass._attr = "b"  # [protected-access]

        Issue3066._bar(i)
        Issue3066.Aclass._bar(i)  # [protected-access]
        Issue3066.Aclass.Bclass._bar(i)  # [protected-access]

    class Aclass:
        """Inner class for GitHub issue 3066"""

        _attr = "x"

        @staticmethod
        def foobar(i):
            """Test access from inner class"""
            Issue3066._attr = 2  # [protected-access]
            Issue3066.Aclass._attr = "y"
            Issue3066.Aclass.Bclass._attr = "b"  # [protected-access]

            Issue3066._bar(i)  # [protected-access]
            Issue3066.Aclass._bar(i)
            Issue3066.Aclass.Bclass._bar(i)  # [protected-access]

        @staticmethod
        def _bar(i):
            """Docstring."""

        class Bclass:
            """Inner inner class for GitHub issue 3066"""

            _attr = "a"

            @staticmethod
            def foobar(i):
                """Test access from inner inner class"""
                Issue3066._attr = 2  # [protected-access]
                Issue3066.Aclass._attr = "y"  # [protected-access]
                Issue3066.Aclass.Bclass._attr = "b"

                Issue3066._bar(i)  # [protected-access]
                Issue3066.Aclass._bar(i)  # [protected-access]
                Issue3066.Aclass.Bclass._bar(i)

            @staticmethod
            def _bar(i):
                """Docstring."""
