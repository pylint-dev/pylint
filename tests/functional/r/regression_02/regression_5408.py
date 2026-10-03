"""Regression test for issue 5408.

Recursion error for self-referencing class attribute.
See: https://github.com/pylint-dev/pylint/issues/5408
"""

# pylint: disable=missing-docstring, too-few-public-methods, invalid-name, inherit-non-class
# pylint: disable=no-self-argument


class MyInnerClass:
    ...


class MySubClass:
    inner_class = MyInnerClass


class MyClass:
    sub_class = MySubClass()


def get_unpatched_class(cls):
    return cls


def get_unpatched(item):
    lookup = get_unpatched_class if isinstance(item, type) else lambda item: None
    return lookup(item)


_Child = get_unpatched(MyClass.sub_class.inner_class)


class Child(_Child):
    def patch(cls):
        MyClass.sub_class.inner_class = cls
