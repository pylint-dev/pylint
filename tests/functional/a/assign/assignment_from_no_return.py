# pylint: disable=missing-docstring


def some_func():
    pass


def decorate(func):
    """Decorate *fn* to return ``self`` to enable chained method calls."""
    def wrapper(self, *args, **kw):
        func(self, *args, **kw)
        return 42
    return wrapper


class Class:

    def some_method(self):
        pass

    @decorate
    def some_other_decorated_method(self):
        pass

    def some_other_method(self):
        value = self.some_method()  # [assignment-from-no-return]
        other_value = self.some_other_decorated_method()
        return value + other_value


VALUE = some_func() # [assignment-from-no-return]


class Parent:
    """Parent class"""

    def compute(self):
        """This isn't supported by all child classes"""

        # pylint: disable=no-self-use
        raise ValueError('Not supported for this object')

    def test(self):
        """Test"""

        result = self.compute()
        return result


class Child(Parent):
    """Child class"""

    def compute(self):
        """This is supported for this child class"""

        return 42
