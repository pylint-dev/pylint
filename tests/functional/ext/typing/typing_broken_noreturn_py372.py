"""
'typing.NoReturn' is broken inside compond types for Python 3.7.0
https://bugs.python.org/issue34921

If no runtime introspection is required, use string annotations instead.

Don't emit errors if py-version set to >= 3.7.2.
"""
# pylint: disable=missing-docstring
import typing
from typing import Callable, NoReturn, Union

import typing_extensions


def func1() -> NoReturn:
    raise Exception

def func2() -> Union[None, NoReturn]:
    pass

def func3() -> Union[None, "NoReturn"]:
    pass

def func4() -> Union[None, typing.NoReturn]:
    pass

def func5() -> Union[None, typing_extensions.NoReturn]:
    pass


Alias1 = NoReturn
Alias2 = Callable[..., NoReturn]
Alias3 = Callable[..., "NoReturn"]
