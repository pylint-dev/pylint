"""Tests for iterating-modified messages"""

# pylint: disable=not-callable,unnecessary-comprehension,too-few-public-methods,missing-class-docstring,missing-function-docstring

import copy
import os
from enum import Enum

item_list = [1, 2, 3]
for item in item_list:
    item_list.append(item)  # [modified-iterating-list]

for item in item_list:
    item_list.remove(item)  # [modified-iterating-list]

for item in item_list.copy():
    item_list.append(item)
    item_list.remove(item)

for item in copy(item_list):
    item_list.append(item)
    item_list.remove(item)

for item in [k for k in item_list]:
    item_list.append(item)
    item_list.remove(item)

MY_DICT = {"1": 1, "2": 2, "3": 3}
i = 1
for item in MY_DICT:
    item_list[0] = i  # for coverage, see reference at /pull/5628#discussion_r792181642
    MY_DICT[i] = 1  # [modified-iterating-dict]
    i += 1

i = 1
for item in MY_DICT.copy():
    MY_DICT[i] = 1
    i += 1

item_set = {1, 2, 3}
for item in item_set:
    item_set.add(item + 10)  # [modified-iterating-set]

item_set = {1, 2, 3}
for item in item_set:
    item_set.clear()  # [modified-iterating-set]

item_set = {1, 2, 3}
for item in item_set:
    item_set.discard(1)  # [modified-iterating-set]

item_set = {1, 2, 3}
for item in item_set:
    item_set.pop()  # [modified-iterating-set]

item_set = {1, 2, 3}
for item in item_set:
    item_set.remove()  # [modified-iterating-set]

for item in item_set.copy():
    item_set.add(item + 10)

for l in item_list:
    for s in item_set:
        item_list.append(1)  # [modified-iterating-list]
        item_set.remove(4)  # [modified-iterating-set]
    item_list.remove(1)  # [modified-iterating-list]

for item in [1, 2, 3]:
    del item  # [modified-iterating-list]

for inner_first, inner_second in [[1, 2], [1, 2]]:
    del inner_second  # [modified-iterating-list]

for k in MY_DICT:
    del k  # [modified-iterating-dict]

for element in item_set:
    del element  # [modified-iterating-set]

# Check for nested for loops and changes to iterators
for l in item_list:
    item_list.append(1)  # [modified-iterating-list]
    for _ in []:
        for _ in []:
            item_list.remove(1)  # [modified-iterating-list]
            for _ in []:
                item_list.append(1)  # [modified-iterating-list]


def format_manifest_serializer_errors(errors):
    """Regression test for issue #5969 - iter_obj is a function call."""
    errors_messages = []
    for key, value in errors.items():
        for message in format_manifest_serializer_errors(value):
            error_message = f"{key}: {message}"
            errors_messages.append(error_message)
    return errors_messages


DICT1 = {"1": 1}
DICT2 = {"2": 2}
for item in DICT1:
    DICT2[item] = 1


def update_existing_key():
    """No message when updating existing keys"""
    for key in MY_DICT:
        MY_DICT[key] = 1

    for key in MY_DICT:
        new_key = key.lower()
        MY_DICT[new_key] = 1  # [modified-iterating-dict]


class MyClass:
    """Regression test for https://github.com/pylint-dev/pylint/issues/7380"""

    def __init__(self) -> None:
        self.attribute = [1, 2, 3]

    def my_method(self):
        """This should raise as we are deleting."""
        for var in self.attribute:
            del var  # [modified-iterating-list]


class MyClass2:
    """Regression test for https://github.com/pylint-dev/pylint/issues/7461"""

    def __init__(self) -> None:
        self.attribute = {}

    def my_method(self):
        """This should not raise, as a copy was made."""
        for key in self.attribute:
            tmp = self.attribute.copy()
            tmp[key] = None


def my_call():
    """Regression test for https://github.com/pylint-dev/pylint/issues/7461"""
    for var in {}.copy():
        del var  # [modified-iterating-dict]


class MyEnum(Enum):
    FOO = 1
    BAR = 2


class EnumClass:
    ENUM_SET = {MyEnum.FOO, MyEnum.BAR}

    def useless(self):
        other_set = set(self.ENUM_SET)
        for obj in self.ENUM_SET:
            other_set.remove(obj)


def django_models_base(fields):
    """Regression test for https://github.com/pylint-dev/pylint/issues/9192."""
    prefetched_objects_cache = {}
    for field in fields:
        if field in prefetched_objects_cache:
            del prefetched_objects_cache[field]
            fields.remove(field)  # [modified-iterating-list]


def is_ignored_path(path):
    return path.startswith(".")


for dirpath, dirnames, _filenames in os.walk(".", topdown=True):
    for dirname in dirnames:
        if is_ignored_path(os.path.join(dirpath, dirname)):
            dirnames.remove(dirname)  # [modified-iterating-list]


def modify_different_uninferable(fields, other):
    """No message when a different uninferable name is modified."""
    for field in fields:
        other.remove(field)
        other.append(field)


def non_modifier_on_uninferable(fields):
    """No message when an uninferable iterated name is not mutated."""
    for field in fields:
        fields.index(field)


def shadowed_uninferable_binding(fields):
    """No message when the receiver is a different binding of the same name."""
    for field in fields:

        def inner(fields):
            fields.remove(None)

        inner(field)


def modify_while_iterating_attribute(container, items):
    """No message when the iterated object is an attribute rather than a name."""
    for entry in container.items:
        items.remove(entry)


def ambiguous_iterated_value(cond):
    """Emit when inference of the iterated name is ambiguous."""
    values = [1, 2, 3] if cond else {1, 2, 3}
    for value in values:
        values.remove(value)  # [modified-iterating-list]
