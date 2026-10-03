class Fruit:
    def __init__(self, name="fruit"):
        self.name = name
        print("Creating a {self.name}")


class Apple(Fruit):
    def __init__(self):
        super().__init__("apple")
