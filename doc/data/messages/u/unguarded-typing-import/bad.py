from collections.abc import Callable  # [unguarded-typing-import]


def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)
