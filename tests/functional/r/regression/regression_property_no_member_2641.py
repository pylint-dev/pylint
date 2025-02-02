# pylint: disable=missing-docstring,unused-argument,too-few-public-methods
# https://github.com/pylint-dev/pylint/issues/2641
from abc import ABCMeta, abstractmethod


class Person(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value


class Myself(Person):
    def __init__(self, name, age, tel):
        super().__init__(name, age)
        self.tel = tel

    @Person.name.setter
    def name(self, value):
        super(self.__class__, self.__class__).name.fset(self, "override")


class Wife(Person):
    def __init__(self, name, age, tel):
        super().__init__(name, age)
        self.tel = tel


MS = Myself("Matheus Saraiva", 36, "988070350")
WI = Wife("Joice Saraiva", 34, "999923554")

print(WI.name)
