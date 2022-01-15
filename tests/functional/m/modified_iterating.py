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
