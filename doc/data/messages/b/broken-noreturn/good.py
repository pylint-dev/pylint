from typing import NoReturn


def exploding_apple(apple) -> NoReturn:
    print(f"{apple} is about to explode")
    raise Exception("{apple} exploded !")
