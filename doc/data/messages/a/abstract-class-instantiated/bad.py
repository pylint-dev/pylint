import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self):
        """Return the sound the animal makes."""
        raise NotImplementedError


class Sheep(Animal):
    def make_sound(self):
        return "baa"


sheep = Sheep()
