"""Names bound by an earlier item of a ``with`` statement can be used by later items.

https://github.com/pylint-dev/pylint/issues/7545
"""
# pylint: disable=missing-function-docstring, unused-variable
import contextlib


@contextlib.contextmanager
def pair():
    yield ("A", "B")


@contextlib.contextmanager
def single(_):
    yield "C"


def name_target():
    with pair() as first, single(first) as second:
        print(first, second)


def tuple_target():
    with pair() as (first, second), single(first) as third:
        print(first, second, third)


def parenthesized_items():
    with (
        pair() as (first, second),
        single(second) as third,
    ):
        print(first, second, third)


def list_target():
    with pair() as [first, second], single(second) as third:
        print(first, second, third)


def nested_and_starred_targets():
    with pair() as (first, *rest), single(rest) as (third, (fourth, fifth)):
        print(first, rest, third, fourth, fifth)


def used_in_own_item():
    with single(first) as (first, second):  # [used-before-assignment]
        print(first, second)


def used_before_later_item():
    with single(third) as first, pair() as (second, third):  # [used-before-assignment]
        print(first, second, third)
