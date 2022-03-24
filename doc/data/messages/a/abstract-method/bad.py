class Pet:
    def make_sound(self):
        raise NotImplementedError


class Cat(Pet):  # [abstract-method]
    pass


import abc


class WildAnimal:
    @abc.abstractmethod
    def make_sound(self):
        pass


class Panther(WildAnimal):  # [abstract-method]
    pass
