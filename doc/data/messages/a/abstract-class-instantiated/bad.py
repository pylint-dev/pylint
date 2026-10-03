import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self):
        pass


sheep = Animal()  # [abstract-class-instantiated]
