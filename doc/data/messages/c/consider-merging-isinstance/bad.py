from typing import Any


def is_number(value: Any) -> bool:
    # +1: [consider-merging-isinstance]
    return isinstance(value, int) or isinstance(value, float)
