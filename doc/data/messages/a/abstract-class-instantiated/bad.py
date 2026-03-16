import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self):
        pass


def demo():
    sheep = Animal()  # [abstract-class-instantiated]
    return sheep
