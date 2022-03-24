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
    def quack(self, decibel, battery=None):
        if battery:
            print(f"Qu{'a' * decibel}ck")
        else:
            print("")
