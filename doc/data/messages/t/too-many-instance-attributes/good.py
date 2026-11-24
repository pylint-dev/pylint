import dataclasses
import typing


class Bar(typing.NamedTuple):
    one: int
    two: int
    three: int
    four: int
    five: int
    six: int
    seven: int
    eight: int
    nine: int
    ten: int
    eleven: int
    twelve: int
    thirteen: int


@dataclasses.dataclass
class Worm:
    name: str
    type: str
    color: str


@dataclasses.dataclass
class Foo:
    one: int
    two: int
    three: int
    four: int
    five: int
    six: int
    seven: int
    eight: int
    nine: int
    ten: int
    eleven: int
    twelve: int
    thirteen: int


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
