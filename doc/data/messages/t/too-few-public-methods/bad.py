class Worm:  # [too-few-public-methods]
    def __init__(self, name: str, fruit_of_residence: Fruit):
        self.name = name
        self.fruit_of_residence = fruit_of_residence

    def bore(self):
        print(f"{self.name} is boring into {self.fruit_of_residence}")
