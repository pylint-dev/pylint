"""
'collections.abc.Callable' is broken inside Optional and Union types for Python 3.9.0
https://bugs.python.org/issue42965

Use 'typing.Callable' instead.
"""
# pylint: disable=missing-docstring,unsubscriptable-object,invalid-name
from __future__ import annotations

import collections.abc
from collections.abc import Callable
from typing import Optional, Union

Alias1 = Optional[Callable[[int], None]]  # [broken-collections-callable]
Alias2 = Union[Callable[[int], None], None]  # [broken-collections-callable]

Alias3 = Optional[Callable[..., None]]
Alias4 = Union[Callable[..., None], None]
Alias5 = list[Callable[[int], None]]
Alias6 = Callable[[int], None]


def func1() -> Optional[Callable[[int], None]]:
    ...

def func2() -> Optional["Callable[[int], None]"]:
    ...

def func3() -> Union[collections.abc.Callable[[int], None], None]:
    ...
