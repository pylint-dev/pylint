class Colour:
    ...


class Red(Colour):
    ...


class Green(Colour):
    ...


class Blue(Colour):
    ...


class Magenta(Colour):
    ...


def is_primary_color(colour: Colour) -> bool:
    return isinstance(colour, (Red, Blue, Green))
