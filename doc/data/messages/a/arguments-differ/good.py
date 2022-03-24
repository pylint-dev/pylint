class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width


class Square(Rectangle):
    def __init__(self, length, width):
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
