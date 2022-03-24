class MyClass:
    def my_abstract_method(self):
        raise NotImplementedError


class ParentClass(MyClass):
    def my_abstract_method(self):
        pass


import abc


class AnotherClass:
    @abc.abstractmethod
    def my_abstract_method(self):
        pass


class AnotherParentClass(AnotherClass):
    def my_abstract_method(self):
        pass
