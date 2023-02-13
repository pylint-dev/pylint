from typing import NamedTuple


class FelidaeCharacteristics(NamedTuple):
    tail_length_cm: int
    paws: int
    eyes: int
    hat: str | None


FELIDAES = {
    "The queen's cymric, fragile furry friend": FelidaeCharacteristics(
        tail_length_cm=1, paws=4, eyes=2, hat="Elizabethan collar"
    ),
    "Rackat the red, terror of the sea": FelidaeCharacteristics(
        tail_length_cm=21, paws=3, eyes=1, hat="Red Hat"
    ),
}
