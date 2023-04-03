class Fruit:
    FRUITS = {"apple": "red", "orange": "orange"}

    def __print_color(self, name, color):
        print(f"{name}: {color}")

    def print(self):
        for fruit, color in self.FRUITS.items():
            self.__print_color(fruit, color)
