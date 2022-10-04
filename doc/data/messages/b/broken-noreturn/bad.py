from typing import NoReturn, Union

def func2() -> Union[None, NoReturn]:  # [broken-noreturn]
    pass