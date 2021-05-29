# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
from collections import defaultdict

class A:
    pass

class B:
    pass

A.__class__ = B
A.__class__ = str
A.__class__ = float
A.__class__ = dict
A.__class__ = set

A.__class__ = defaultdict
A.__class__ = defaultdict(str)  # [invalid-class-object]
A.__class__ = 1  # [invalid-class-object]
