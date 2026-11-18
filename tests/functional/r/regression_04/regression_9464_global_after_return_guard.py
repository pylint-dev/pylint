"""Regression test for https://github.com/pylint-dev/pylint/issues/9464

After ``if var is None: return``, a global Optional[int] is an int, so
``-var`` is fine, as it already was with an ``else`` branch. Fixed in astroid
by pylint-dev/astroid#3387.
"""

# pylint: disable=missing-docstring,global-statement,invalid-name

import random
from typing import Optional

var: Optional[int] = None


def maybe_modify() -> None:
    global var
    if random.randint(0, 1) == 0:
        var = 1


def with_return_guard() -> None:
    maybe_modify()
    if var is None:
        return
    print(-var)


def with_else() -> None:
    maybe_modify()
    if var is None:
        pass
    else:
        print(-var)
