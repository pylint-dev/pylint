class Fruit:
    def __init__(self):
        print("Fruit")


class Apple(Fruit):
    def __init__(self):
        super().__init__()
        print("Apple")
