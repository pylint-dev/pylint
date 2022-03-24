import abc


class BaseClass(abc.ABC):
    @abc.abstractmethod
    def get_something(self):
        pass


class MyClass(BaseClass):
    def get_something(self):
        pass


foo = MyClass()
