# pylint: disable=missing-docstring
from json import JSONEncoder

class Control: # [too-few-public-methods]
    ...


class MyJsonEncoder(JSONEncoder):
    ...

class InheritedInModule(Control):
    """This class inherits from a class that doesn't have enough methods,
    and its parent is excluded via config, so it doesn't raise."""
