"""Tests for iterating-modified messages"""
# pylint: disable=not-callable,unnecessary-comprehension

import copy

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
    my_dict[i] = 1      # [modified-iterating-dict]
    i += 1

i = 1
for item in my_dict.copy():
    my_dict[i] = 1
    i += 1

item_set = {1, 2, 3}
for item in item_set:
    item_set.add(item + 10)  # [modified-iterating-set]

for item in item_set.copy():
    item_set.add(item + 10)

for l in item_list:
    for s in item_set:
        item_list.append(1)  # [modified-iterating-list]
        item_set.remove(4)  # [modified-iterating-set]
    item_list.remove(1)  # [modified-iterating-list]

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
