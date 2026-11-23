"""Targets of an assignment are bound left to right, after the value is evaluated.

So a name read inside a target can use a name bound by an earlier target.
https://github.com/pylint-dev/pylint/issues/5955
"""
# pylint: disable=missing-function-docstring, unused-variable, invalid-name

b = {}
a = b[id(a)] = 0

items = [10]
x = y = items[x] = 0
c, items[c] = 0, 20
items[d], d = 20, 0  # [used-before-assignment]
b[id(e)] = e = 0  # [used-before-assignment]


def chained_targets(store):
    first = store[first] = 0
    second = third = store[second] = 0
    return first, second, third


def tuple_target(store):
    first, store[first] = 0, 1
    return first


def starred_target(store):
    first, *store[first:] = 1, 2, 3
    return first


def nested_tuple_target(store):
    (first, (store[first], second)) = 1, (2, 3)
    return first, second


def attribute_target(obj):
    first = obj.items[first] = 0
    return first


def name_read_before_its_target(store):
    store[first], first = 1, 0  # [used-before-assignment]
    return first


def name_read_by_earlier_target(store):
    store[first] = first = 0  # [used-before-assignment]
    return first


def name_bound_in_comprehension(store, values):
    store[len([0 for first in values]), first] = first = 0  # [used-before-assignment]
    return first


def name_bound_in_lambda(store):
    store[(lambda first: first), first] = first = 0  # [used-before-assignment]
    return first


def name_read_in_value(store):
    first = store[0] = second  # [used-before-assignment]
    second = 1
    return first, second


def name_bound_by_later_statement(store):
    store[first] = 0  # [used-before-assignment]
    first = 1
    return first
