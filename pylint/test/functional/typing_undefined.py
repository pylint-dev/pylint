# pylint: disable=missing-docstring
from __future__ import (
    absolute_import,
    division,
    print_function,
)

# pylint: disable=line-too-long

def func_1(arg1, arg2):
    # type: (Set[int], Set[int]) -> Set[int]  # [undefined-variable,undefined-variable,undefined-variable]
    var = None  # type: Optional[Set[int]]  # [undefined-variable,undefined-variable]
    assert arg2
    if arg1:
        var = {1, 2, 3}
    return var

def add(arg1,  # type: List[int]  # [undefined-variable]
        arg2   # type: int
       ):
    # type: (...) -> int
    return arg1[0] + arg2

def do_nothing():
    # type: () -> None
    pass

class Awesome(object):

    DATA = []  # type: List[str] # [undefined-variable]

    def __init__(self, data):
        # type: (str) -> None
        self.data = data
        self.arg = None  # type: Optional[datetime.date] # [undefined-variable,undefined-variable]

    def set(self, arg, data):
        # type: (datetime.date, str) -> None # [undefined-variable]
        self.arg = arg
        self.data = data

    def get(self, arg):
        # type: (int) -> str
        return self.data[arg]
