import abc


class WildAnimal:
    @abc.abstractmethod
    def make_sound(self):
        pass


class Panther(WildAnimal):
    def make_sound(self):
        print("MEEEOW")
