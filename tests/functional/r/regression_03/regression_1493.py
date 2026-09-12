# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/1493

Calling a value taken from a container that also holds ``None`` should not
trigger not-callable when the call is guarded by an ``is not None`` check.

Reproducible up to pylint 2.14; fixed in pylint 2.15.0.
"""

# pylint: disable=missing-docstring,too-few-public-methods
cfg = [
    {"v": [0, 1], "f": None},
    {"v": [1, 2], "f": sum},
]

for c in cfg:
    if c["f"] is not None:
        c["f"](c["v"])


class Test:
    _func = None

    def test(self):
        if self._func is not None:
            return self._func()
        return None
