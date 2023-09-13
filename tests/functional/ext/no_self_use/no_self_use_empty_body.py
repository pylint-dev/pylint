# pylint: disable=missing-docstring,too-few-public-methods

class LivingThing:
    def make_sound(self):
        raise NotImplementedError

class Cow(LivingThing):
    def make_sound(self):  # [no-self-use]
        print("Moooh. Moomoo.")

class Plant(LivingThing):
    def make_sound(self):  # [no-self-use]
        pass

class Base:
    """an abstract class"""

    def pass_only(self):  # [no-self-use]
        # non-docstring because having one affects the result here
        # this method isn't a real method since it doesn't need self
        pass

    def docstring_only(self):  # [no-self-use]
        """this method isn't a real method since it doesn't need self"""
