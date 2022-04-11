import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self):
        pass


class Sheep(Animal):
    def make_sound(self):
        print("bhaaaaa")


sheep = Sheep()
