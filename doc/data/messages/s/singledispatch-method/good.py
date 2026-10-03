from functools import singledispatch


@singledispatch
def convert_position(position):
    print(position)


@convert_position.register
def _(position: str) -> tuple:
    position_a, position_b = position.split(",")
    return (int(position_a), int(position_b))


@convert_position.register
def _(position: tuple) -> str:
    return f"{position[0]},{position[1]}"
