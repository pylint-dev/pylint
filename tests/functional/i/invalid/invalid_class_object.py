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


def get_pair():
    return AnotherClass, "myvalue"


class CrashRegression11267:
    """``x.__class__`` targets outside a plain assignment used to crash.

    See https://github.com/pylint-dev/pylint/issues/11267
    """

    def dunder_class_as_loop_target(self):
        for self.__class__ in [AnotherClass]:
            pass

    def dunder_class_as_tuple_loop_target(self):
        for self.__class__, myvar in [(AnotherClass, "myvalue")]:
            print(myvar)

    def dunder_class_as_with_target(self, ctx):
        with ctx as self.__class__:
            pass

    def dunder_class_as_comprehension_target(self):
        return [0 for self.__class__ in [AnotherClass]]

    def dunder_class_annotation_without_value(self):
        self.__class__: type

    def dunder_class_unpacked_from_call(self):
        self.__class__, myvar = get_pair()
        print(myvar)

    def dunder_class_in_nested_tuple_target(self, other):
        (other.attr, self.__class__), myvar = (1, AnotherClass), 2
        print(myvar)

    def dunder_class_unbalanced_unpacking(self):
        # pylint: disable-next=unbalanced-tuple-unpacking
        myvar, self.__class__ = (AnotherClass,)
        print(myvar)

    def dunder_class_in_list_target(self):
        [self.__class__, myvar] = 1, 2  # [invalid-class-object]
        print(myvar)

    def dunder_class_in_list_target_good(self):
        [self.__class__, myvar] = AnotherClass, 2
        print(myvar)

    def dunder_class_as_starred_target(self):
        *self.__class__, myvar = [1, 2]  # [invalid-class-object]
        print(myvar)

    def dunder_class_as_trailing_starred_target(self, other):
        other.attr, *self.__class__ = [1, 2]  # [invalid-class-object]

    def dunder_class_as_starred_loop_target(self):
        for *self.__class__, myvar in [[1, 2]]:  # [invalid-class-object]
            print(myvar)
