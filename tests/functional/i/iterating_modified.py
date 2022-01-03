"""Tests for iterating-modified messages"""
# pylint disable=locally-disabled,useless-suppression

item_list = [1, 2, 3]
for item in item_list:
    item_list.append(item)  # [iterating-modified-list]

for item in item_list.copy():
    item_list.append(item)

for item in item_list:
    item_list.remove(item)  # [iterating-modified-list]
    print(item)

my_dict = {"1": 1, "2": 2, "3": 3}
i = 1
for item in my_dict:
    my_dict[i] = 1
    i += 1

i = 1
for item in my_dict.copy():
    my_dict[i] = 1
    i += 1

item_set = {1, 2, 3}
for item in item_set:
    item_set.add(item + 10)

for item in item_set.copy():
    item_set.add(item + 10)
