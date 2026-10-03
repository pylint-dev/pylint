class Fruit:  # [eq-without-hash]
    def __init__(self) -> None:
        self.name = "apple"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Fruit) and other.name == self.name
