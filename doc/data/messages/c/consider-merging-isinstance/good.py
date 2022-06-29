from typing import Any


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float))
