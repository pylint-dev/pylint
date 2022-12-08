class Fruit:
    def __init__(self) -> None:
        self.name = "apple"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Fruit) and other.x == self.x

    def __hash__(self) -> int:
        return hash(self.name)
