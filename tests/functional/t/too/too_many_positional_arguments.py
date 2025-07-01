# pylint: disable=missing-function-docstring, missing-module-docstring
class RegularMethods:
    """The max positional arguments default is 5. Regular methods doesn't count `self`."""
    # +1: [too-many-arguments, too-many-positional-arguments]
    def regular_fail1(self, a, b, c, d, e, f):
        pass
    # +1: [too-many-arguments, too-many-positional-arguments]
    def regular_fail2(self, a, b, c, d, e, /, f):
        pass
    # +1: [too-many-arguments]
    def regular_okay1(self, a, b, c, d, e, *, f=True):
        pass
    def regular_okay2(self, a, b, c, d, e):
        pass
