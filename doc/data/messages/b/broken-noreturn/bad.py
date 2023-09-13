from typing import NoReturn, Union


def exploding_apple(apple) -> Union[None, NoReturn]:  # [broken-noreturn]
    print(f"{apple} is about to explode")
