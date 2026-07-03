import dataclasses


@dataclasses.dataclass
class Worm:
    name: str
    type: str
    color: str


class Fruit:
    def __init__(self):
        self.name = "Little Apple"
        self.color = "Bright red"
        self.vitamins = ["A", "B1"]
        self.antioxidants = None
        self.worms = [
            Worm(name="Jimmy", type="Codling Moths", color="light brown"),
            Worm(name="Kim", type="Apple maggot", color="Whitish"),
        ]
