"""Warning about assigning self/cls variable."""
from __future__ import print_function
# pylint: disable=too-few-public-methods, useless-object-inheritance

class Foo(object):
    """Class with methods that check for self/cls assignment"""

    # pylint: disable=no-self-argument,no-self-use
    def self_foo(bar_):
        """Instance method, should warn for bar"""
        bar_ = 10  # [self-cls-assignment]

    # pylint: disable=no-self-use
    def self_foofoo(self, lala):
        """Instance method, should warn for self"""
        self = lala  # [self-cls-assignment]

    @classmethod
    def cls_foo(cls):
        """Class method, should warn for cls"""
        cls = 'tada'  # [self-cls-assignment]

    # pylint: disable=unused-argument
    @staticmethod
    def static_foo(lala):
        """Static method, no warnings"""
        lala = 10


# pylint: disable=unused-argument
def free_foo(bar_, lala):
    """Free function, no warnings"""
    bar_ = lala


class TestNonLocal:
    """Test class for nonlocal assignment of self"""

    def function(self, param):
        """This function uses nonlocal to reassign self"""

        def _set_param(param):
            nonlocal self
            self = param  # [self-cls-assignment]

        _set_param(param)
        return self
