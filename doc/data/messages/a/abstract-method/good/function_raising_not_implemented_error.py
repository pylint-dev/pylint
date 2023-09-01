class Pet:
    def make_sound(self):
        raise NotImplementedError


class Cat(Pet):
    def make_sound(self):
        print("Meeeow")
