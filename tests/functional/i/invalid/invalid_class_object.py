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


# Here, ambiguity is found when inferring self.__class__
class C:
    @classmethod
    def _new_instance(cls):
        obj = C()
        obj.__class__ = cls
        return obj

    def __deepcopy__(self, memo):
        obj = C()
        obj.__class__ = self.__class__
        return obj
