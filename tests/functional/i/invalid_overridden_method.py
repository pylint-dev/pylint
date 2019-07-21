# pylint: disable=missing-docstring, too-few-public-methods
import abc


class SuperClass(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def prop(self):
        pass

    @abc.abstractmethod
    def method(self):
        pass


class Prop(SuperClass):
    @property
    def prop(self):
        return None

    def method(self):
        pass


class NoProp(SuperClass):
    def prop(self):  # [invalid-overridden-method]
        return None

    @property
    def method(self): # [invalid-overridden-method]
        return None


class Property:

    @property
    def close(self):
        pass


class PropertySetter(Property):

    @property
    def close(self):
        pass

    @close.setter
    def close(self, attr):
        return attr

    @close.deleter
    def close(self):
        return None
