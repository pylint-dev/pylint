# pylint: disable=missing-function-docstring, missing-module-docstring
class FiveArgumentMethods:
    """The max positional arguments default is 5."""
    def fail1(self, a, b, c, d, e):  # [too-many-arguments, too-many-positional-arguments]
        pass
    def fail2(self, a, b, c, d, /, e):  # [too-many-arguments, too-many-positional-arguments]
        pass
    def okay1(self, a, b, c, d, *, e=True):  # [too-many-arguments]
        pass
