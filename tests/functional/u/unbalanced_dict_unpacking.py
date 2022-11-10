# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
# pylint: disable=unused-variable, redefined-outer-name, line-too-long

def dict_vals():
    a, b, c, d, e, f, g = {1: 2}.values()  # [unbalanced-dict-unpacking]
    return a, b

def dict_keys():
    a, b, c, d, e, f, g = {1: 2, "hi": 20}.keys()  # [unbalanced-dict-unpacking]
    return a, b


def dict_items():
    tupe_one, tuple_two = {1: 2, "boo": 3}.items()
    tupe_one, tuple_two, tuple_three = {1: 2, "boo": 3}.items()  # [unbalanced-dict-unpacking]
    return tuple_three

def all_dict():
    a, b, c, d, e, f, g = {1: 2, 3: 4}  # [unbalanced-dict-unpacking]
    good = {1: 2}
    return good

for a, b, c, d, e, f, g in {1: 2}.items():  # [unbalanced-dict-unpacking]
    pass

for a, b, c, d, e, f, g in {1: 2}:  # [unbalanced-dict-unpacking]
    pass

for a, b, c, d, e, f, g in {1: 2}.keys():  # [unbalanced-dict-unpacking, consider-iterating-dictionary]
    pass

for a, b, c, d, e, f, g in {1: 2}.values():  # [unbalanced-dict-unpacking]
    pass
