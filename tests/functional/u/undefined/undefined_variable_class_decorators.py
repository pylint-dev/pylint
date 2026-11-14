"""Class decorators are evaluated in the scope that encloses the class, see #7720."""
# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods


def identity(cls):
    return cls


class Container:
    register = identity

    @register
    class Plain:
        pass

    @register
    @register
    class Stacked:
        pass

    class Inner:
        nested_register = identity

        @nested_register
        class Nested:
            pass


# The decorator is evaluated before the body of the decorated class is run.
@only_in_body  # [undefined-variable]
class Decorated:
    only_in_body = identity
