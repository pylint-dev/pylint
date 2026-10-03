from collections.abc import Callable
from typing import Optional


def func() -> Optional[Callable[[int], None]]:  # [broken-collections-callable]
    ...
