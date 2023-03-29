"""Regression test for a crash reported in https://github.com/pylint-dev/pylint/issues/4982"""
# pylint: disable=too-few-public-methods

class Base:
    """A class"""
    @classmethod
    def get_first_subclass(cls):
        """Return the first subclass of this class"""
        for subklass in cls.__subclasses__():
            return subklass
        return object


subclass = Base.get_first_subclass()


class Another(subclass):
    """Create a class from the __subclasses__ attribute of another class"""
