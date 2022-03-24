import abc


class BaseClass(abc.ABC):
    @abc.abstractmethod
    def get_something(self):
        pass


foo = BaseClass()  # [abstract-class-instantiated]
