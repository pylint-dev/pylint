# pylint: disable=missing-function-docstring, missing-module-docstring
class RegularMethods:
    """The max positional arguments default is 5. Regular methods don't count `self`."""

    # +1: [too-many-arguments, too-many-positional-arguments]
    def regular_fail1(self, a, b, c, d, e, f):
        pass
    # +1: [too-many-arguments, too-many-positional-arguments]
    def regular_fail2(self, a, b, c, d, e, /, f):
        pass
    # +1: [too-many-arguments, too-many-positional-arguments]
    def regular_fail3(self, /, a, b, c, d, e, f):
        pass
    # +1: [too-many-arguments]
    def regular_soso1(self, a, b, c, d, e, *, f=True):
        pass
    # +1: [too-many-arguments]
    def regular_soso2(self, a, b, c, d, e, /, *, f=True):
        pass
    # +1: [too-many-arguments]
    def regular_soso3(self, /, a, b, c, d, e, *, f=True):
        pass
    # +1: [too-many-arguments]
    def regular_soso4(self, a, b, c, d, e, /, _f, *, g=True):
        pass
    # +1: [too-many-arguments]
    def regular_soso5(self, /, _a, b, c, d, e, f, *, g=True):
        pass
    def regular_okay1(self, a, b, c, d, e):
        pass
    def regular_okay2(self, a, b, c, d, e, /):
        pass
    def regular_okay3(self, *, a, b, c, d, e):
        pass
    def regular_okay4(self, a, b, c, d, e, /, _f):
        pass
    def regular_okay5(self, _a, b, c, d, e, /, f):
        pass
    def regular_okay6(self, /, _a, b, c, d, e, f):
        pass
    def regular_okay7(self, /, a, b, c, d, e, _f):
        pass


# pylint: disable=missing-function-docstring, missing-module-docstring
class StaticMethods:
    """The max positional arguments default is 5. Static methods count them all."""

    @staticmethod
    # +1: [too-many-arguments, too-many-positional-arguments]
    def static_fail1(a, b, c, d, e, f):
        pass
    @staticmethod
    # +1: [too-many-arguments, too-many-positional-arguments]
    def static_fail2(a, b, c, d, e, /, f):
        pass
    @staticmethod
    # +1: [too-many-arguments]
    def static_soso1(a, b, c, d, e, *, f=True):
        pass
    @staticmethod
    # +1: [too-many-arguments]
    def static_soso2(a, b, c, d, e, /, *, f=True):
        pass
    @staticmethod
    # +1: [too-many-arguments]
    def static_soso3(a, b, c, d, e, /, _f, *, g=True):
        pass
    @staticmethod
    def static_okay1(a, b, c, d, e):
        pass
    @staticmethod
    def static_okay2(a, b, c, d, e, /):
        pass
    @staticmethod
    def static_okay3(*, a, b, c, d, e):
        pass
    @staticmethod
    def static_okay4(a, b, c, d, e, /, _f):
        pass
    @staticmethod
    def static_okay5(_a, b, c, d, e, /, f):
        pass


# pylint: disable=missing-function-docstring, missing-module-docstring
class ClassMethods:
    """The max positional arguments default is 5. Class methods don't count `cls`."""

    @classmethod
    # +1: [too-many-arguments, too-many-positional-arguments]
    def class_fail1(cls, a, b, c, d, e, f):
        pass
    @classmethod
    # +1: [too-many-arguments, too-many-positional-arguments]
    def class_fail2(cls, a, b, c, d, e, /, f):
        pass
    @classmethod
    # +1: [too-many-arguments, too-many-positional-arguments]
    def class_fail3(cls, /, a, b, c, d, e, f):
        pass
    @classmethod
    # +1: [too-many-arguments]
    def class_soso1(cls, a, b, c, d, e, *, f=True):
        pass
    @classmethod
    # +1: [too-many-arguments]
    def class_soso2(cls, a, b, c, d, e, /, *, f=True):
        pass
    @classmethod
    # +1: [too-many-arguments]
    def class_soso3(cls, /, a, b, c, d, e, *, f=True):
        pass
    @classmethod
    # +1: [too-many-arguments]
    def class_soso4(cls, a, b, c, d, e, /, _f, *, g=True):
        pass
    @classmethod
    # +1: [too-many-arguments]
    def class_soso5(cls, /, _a, b, c, d, e, f, *, g=True):
        pass
    @classmethod
    def class_okay1(cls, a, b, c, d, e):
        pass
    @classmethod
    def class_okay2(cls, a, b, c, d, e, /):
        pass
    @classmethod
    def class_okay3(cls, *, a, b, c, d, e):
        pass
    @classmethod
    def class_okay4(cls, a, b, c, d, e, /, _f):
        pass
    @classmethod
    def class_okay5(cls, _a, b, c, d, e, /, f):
        pass
    @classmethod
    def class_okay6(cls, /, _a, b, c, d, e, f):
        pass
    @classmethod
    def class_okay7(cls, /, a, b, c, d, e, _f):
        pass
