"""Annotations and defaults in the signature of a function are evaluated when
the function is defined, so they cannot use a loop variable of its body.
https://github.com/pylint-dev/pylint/issues/5480
"""
# pylint: disable=missing-function-docstring, redefined-builtin, redefined-outer-name
# pylint: disable=unused-argument, invalid-name

from typing import List


def parse_dict(dict_object: List[dict], name: str) -> dict:
    for dict in dict_object:
        if dict.get("name") == name:
            return dict
    return {}


d = list


def argument_annotation(items: d):
    for d in items:
        print(d)


def return_annotation(items) -> d:
    for d in items:
        print(d)
    return []


def nested_in_annotations(items: List[d]) -> List[d]:
    for d in items:
        print(d)
    return []


def other_parameter_kinds(first: d, /, *rest: d, items: d, **extra: d):
    for d in items:
        print(d)


def nested_in_default(items, size=len(d.__name__)):
    for d in items:
        print(d)


def default(items, kind=d):
    for d in items:
        print(d)


async def async_function(items: d) -> d:
    async for d in items:
        print(d)
    return []


def used_after_loop(items):
    for d in items:
        print(d)
    return d  # [undefined-loop-variable]


def used_in_decorator(items):
    for e in items:
        print(e)

    @e  # [undefined-loop-variable]
    def inner():
        pass

    return inner
