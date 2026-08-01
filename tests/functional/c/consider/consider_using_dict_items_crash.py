"""Non-name loop targets must not crash ``consider-using-dict-items``.

https://github.com/pylint-dev/pylint/issues/11173

The ``other[index]`` subscripts below are required to reach the code path that
crashed (the checker only inspects bodies that subscript a name); do not remove
them or this stops covering the bug. None of these forms can be rewritten with
``.items()``, so no message is expected either.
"""

# pylint: disable=missing-docstring

D = {"key": "value"}


def loop_into_attribute(obj, other, index):
    for obj.key in D:
        print(other[index])


def loop_into_attribute_keys(obj, other, index):
    for obj.key in D.keys():  # [consider-iterating-dictionary]
        print(other[index])


def loop_into_subscript(out, other, index):
    for out["k"] in D:
        print(other[index])


def comprehension_into_attribute(obj, other, index):
    return [other[index] for obj.key in D]
