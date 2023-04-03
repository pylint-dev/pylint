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


class AnotherClass:
    ...


class Pylint7429Good:
    """See https://github.com/pylint-dev/pylint/issues/7467"""

    def class_defining_function_good(self):
        self.__class__, myvar = AnotherClass, "myvalue"
        print(myvar)

    def class_defining_function_bad(self):
        self.__class__, myvar = 1, "myvalue"  # [invalid-class-object]
        print(myvar)

    def class_defining_function_good_inverted(self):
        myvar, self.__class__ = "myvalue", AnotherClass
        print(myvar)

    def class_defining_function_bad_inverted(self):
        myvar, self.__class__ = "myvalue", 1  # [invalid-class-object]
        print(myvar)

    def class_defining_function_complex_bad(self):
        myvar, self.__class__, other = (  # [invalid-class-object]
            "myvalue",
            1,
            "othervalue",
        )
        print(myvar, other)

    def class_defining_function_complex_good(self):
        myvar, self.__class__, other = (
            "myvalue",
            str,
            "othervalue",
        )
        print(myvar, other)
