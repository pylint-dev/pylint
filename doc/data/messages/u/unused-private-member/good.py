class Fruit:
    FRUITS = ["apple", "orange"]

    def __print_color(self, name):
        print(f"{name}: red")

    def print(self):
        for fruit in self.FRUITS:
            self.__print_color(fruit)
