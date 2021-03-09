# pylint: disable=missing-docstring, too-few-public-methods
import abc


class SuperClass(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def prop(self):
        pass

    @abc.abstractmethod
    async def async_method(self):
        pass

    @abc.abstractmethod
    def method_a(self):
        pass

    @abc.abstractmethod
    def method_b(self):
        pass

class ValidDerived(SuperClass):
    @property
    def prop(self):
        return None

    async def async_method(self):
        return None

    def method_a(self):
        pass

    def method_b(self):
        pass

class InvalidDerived(SuperClass):
    def prop(self):  # [invalid-overridden-method]
        return None

    def async_method(self): # [invalid-overridden-method]
        return None

    @property
    def method_a(self): # [invalid-overridden-method]
        return None

    async def method_b(self): # [invalid-overridden-method]
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


class AbstractProperty:

    @abc.abstractproperty
    def prop(self):
        return
