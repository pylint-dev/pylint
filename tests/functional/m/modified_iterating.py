"""Tests for iterating-modified messages"""
# pylint: disable=not-callable,unnecessary-comprehension,too-few-public-methods,missing-class-docstring,missing-function-docstring

import copy
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

my_dict = {"1": 1, "2": 2, "3": 3}
i = 1
for item in my_dict:
    item_list[0] = i  # for coverage, see reference at /pull/5628#discussion_r792181642
    my_dict[i] = 1  # [modified-iterating-dict]
    i += 1

i = 1
for item in my_dict.copy():
    my_dict[i] = 1
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

for k in my_dict:
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


dict1 = {"1": 1}
dict2 = {"2": 2}
for item in dict1:
    dict2[item] = 1


def update_existing_key():
    """No message when updating existing keys"""
    for key in my_dict:
        my_dict[key] = 1

    for key in my_dict:
        new_key = key.lower()
        my_dict[new_key] = 1  # [modified-iterating-dict]


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
