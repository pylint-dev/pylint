"""
'collections.abc.Callable' is broken inside Optional and Union types for Python 3.9.0
https://bugs.python.org/issue42965

Use 'typing.Callable' instead.

Don't emit 'deprecated-typing-alias' for 'Callable' if at least one replacement
would create broken instances.
"""
# pylint: disable=missing-docstring,unsubscriptable-object,invalid-name
from typing import Callable, Optional, Union

Alias1 = Optional[Callable[[int], None]]
Alias2 = Union[Callable[[int], None], None]

Alias3 = Optional[Callable[..., None]]
Alias4 = Union[Callable[..., None], None]
Alias5 = list[Callable[[int], None]]
Alias6 = Callable[[int], None]


def func1() -> Optional[Callable[[int], None]]:
    ...

def func2() -> Optional["Callable[[int], None]"]:
    ...
