class Square:
    def set_size(self, length):
        self.length = length


class Rectangle(Square):
    def set_size(self, length, width):  # [arguments-differ]
        self.length = length
        self.width = width


class Duck:
    def quack(self, decibel):
        print(f"Qu{'a' * decibel}ck")


class PlasticDuck(Duck):
    def quack(self, decibel, battery):  # [arguments-differ]
        if battery:
            print(f"Qu{'a' * decibel}ck")
        else:
            print("")
