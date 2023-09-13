import abc


class Animal:
    @abc.classmethod
    @abc.abstractmethod
    def breath(cls):
        pass
