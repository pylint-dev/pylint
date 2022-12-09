class Fruit:
    def __init__(self) -> None:
        self.name = "apple"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Fruit) and other.name == self.name

    def __hash__(self) -> int:
        return hash(self.name)
