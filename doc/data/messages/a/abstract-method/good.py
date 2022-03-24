class Pet:
    def make_sound(self):
        raise NotImplementedError


class Cat(Pet):
    def make_sound(self):
        print("Meeeow")


import abc


class WildAnimal:
    @abc.abstractmethod
    def make_sound(self):
        pass


class Panther(WildAnimal):
    def make_sound(self):
        print("MEEEOW")
