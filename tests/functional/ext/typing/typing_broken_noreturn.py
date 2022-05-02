"""
'typing.NoReturn' is broken inside compond types for Python 3.7.0
https://bugs.python.org/issue34921

If no runtime introspection is required, use string annotations instead.
"""
# pylint: disable=missing-docstring
import typing
from typing import TYPE_CHECKING, Callable, NoReturn, Union

import typing_extensions


def func1() -> NoReturn:
    raise Exception

def func2() -> Union[None, NoReturn]:  # [broken-noreturn]
    pass

def func3() -> Union[None, "NoReturn"]:
    pass

def func4() -> Union[None, typing.NoReturn]:  # [broken-noreturn]
    pass

def func5() -> Union[None, typing_extensions.NoReturn]:  # [broken-noreturn]
    pass


Alias1 = NoReturn
Alias2 = Callable[..., NoReturn]  # [broken-noreturn]
Alias3 = Callable[..., "NoReturn"]

if TYPE_CHECKING:
    # ok inside TYPE_CHECKING block
    Alias4 = Callable[..., NoReturn]
