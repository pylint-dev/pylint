# pylint: disable=missing-module-docstring,missing-class-docstring,too-few-public-methods
# pylint: disable=no-self-use,missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING


class Cls:
    def func(self, stuff: defaultdict):
        # This import makes the definition work.
        # pylint: disable=import-outside-toplevel
        from collections import defaultdict

        obj = defaultdict()
        obj.update(stuff)
        return obj


if TYPE_CHECKING:
    # This import makes the annotations work.
    from collections import defaultdict
