class Rectangle:
    def __init__(self, length):
        self.length = length


class Square(Rectangle):
    def __init__(self, length, width=None):
        self.length = length
        self.width = width


class Duck:
    def quack(self, decibel):
        print(f"Qu{'a' * decibel}ck")


class PlasticDuck:
    """A plastic Duck is not a Duck, they should not inherit from each other."""
    def quack(self, decibel, battery):
        if battery:
            print(f"Qu{'a' * decibel}ck")
        else:
            print("")
