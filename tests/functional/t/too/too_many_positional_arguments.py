# pylint: disable=missing-function-docstring, missing-module-docstring
class FiveArgumentMethods:
    """The max positional arguments default is 5, so 6 for a method because of self."""
    def fail1(self, a, b, c, d, e, f):  # [too-many-arguments, too-many-positional-arguments]
        pass
    def fail2(self, a, b, c, d, e, /, f):  # [too-many-arguments, too-many-positional-arguments]
        pass
    def okay1(self, a, b, c, d, e, *, f=True):  # [too-many-arguments]
        pass
