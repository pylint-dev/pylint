""" Tests for class with dunder attributes. """
# pylint: disable=too-few-public-methods,missing-docstring

class MyClass(object):
    __all__ = ('one', 'two', 'three')  # [dunder-class-attribute]

    regular_attribute = __dunder__ = True  # [dunder-class-attribute]

    __this_is_fine = True

    so_is_this__ = True

    perfectly_fine = 10

    # assigning to predefined attributes is also fine, e.g.
    __doc__ = 'My testing class'

    def __init__(self):
        pass

    def test(self):
        pass
