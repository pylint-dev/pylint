import dataclasses


@dataclasses.dataclass
class Worm:
    name: str
    fruit_of_residence: Fruit


def bore(worm: Worm):
    print(f"{worm.name} is boring into {worm.fruit_of_residence}")
