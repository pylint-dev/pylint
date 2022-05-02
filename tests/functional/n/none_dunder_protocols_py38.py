# pylint: disable=missing-docstring,too-few-public-methods,expression-not-assigned
class MetaContainer(type):
    __contains__ = None


class NamedExpressionClass(metaclass=MetaContainer):
    if (__iter__ := lambda x: x):
        pass


def test():
    1 in NamedExpressionClass()
