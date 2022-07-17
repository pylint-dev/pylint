import dataclasses


class Worm:
    def __init__(self, name: str, fruit_of_residence: Fruit):
        self.name = name
        self.fruit_of_residence = fruit_of_residence

    def bore(self):
        print(f"{self.name} is boring into {self.fruit_of_residence}")

    def wiggle(self):
        print(f"{self.name} wiggle around wormily.")

# or

@dataclasses.dataclass
class Worm:
    name:str
    fruit_of_residence: Fruit

def bore(worm: Worm):
    print(f"{worm.name} is boring into {worm.fruit_of_residence}")

# or

def bore(fruit: Fruit, worm_name: str):
    print(f"{worm_name} is boring into {fruit}")
