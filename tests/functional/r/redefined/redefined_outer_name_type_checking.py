# pylint: disable=missing-module-docstring,missing-class-docstring,too-few-public-methods
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING
import typing as t


class Cls:
    def func(self, stuff: defaultdict, my_deque: deque):
        # These imports make the definition work.
        # pylint: disable=import-outside-toplevel
        from collections import defaultdict
        from collections import deque

        obj = defaultdict()
        obj2 = deque()
        obj.update(stuff)
        obj2.append(my_deque)
        return obj


if TYPE_CHECKING:
    # This import makes the annotations work.
    from collections import defaultdict

if t.TYPE_CHECKING:
    # This import makes the annotations work.
    from collections import deque
