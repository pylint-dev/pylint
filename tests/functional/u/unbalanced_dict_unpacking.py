"""Check possible unbalanced dict unpacking """
# pylint: disable=missing-function-docstring, invalid-name
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
    return a

for a, b, c, d, e, f, g in {1: 2}.items():  # [unbalanced-dict-unpacking]
    pass

for key, value in {1: 2}:  # [unbalanced-dict-unpacking]
    pass

for key, value in {1: 2}.keys():  # [unbalanced-dict-unpacking, consider-iterating-dictionary]
    pass

for key, value in {1: 2}.values():  # [unbalanced-dict-unpacking]
    pass

empty = {}

# this should not raise unbalanced-dict because it is valid code using `items()`
for key, value in empty.items():
    print(key)
    print(value)

for key, val in {1: 2}.items():
    print(key)

populated = {2: 1}
for key, val in populated.items():
    print(key)

key, val = populated.items()  # [unbalanced-dict-unpacking]

for key, val in {1: 2, 3: 4, 5: 6}.items():
    print(key)

key, val = {1: 2, 3: 4, 5: 6}.items()  # [unbalanced-dict-unpacking]

a, b, c = {}  # [unbalanced-dict-unpacking]

for k in {'key': 'value', 1: 2}.items():
    print(k)

for k, _ in {'key': 'value'}.items():
    print(k)

for _, _ in {'key': 'value'}.items():
    print(_)

for _, val in {'key': 'value'}.values():  # [unbalanced-dict-unpacking]
    print(val)

for key, *val in {'key': 'value', 1: 2}.items():
    print(key)

for *key, val in {'key': 'value', 1: 2}.items():
    print(key)


for key, *val in {'key': 'value', 1: 2, 20: 21}.values():  # [unbalanced-dict-unpacking]
    print(key)

for *key, val in {'key': 'value', 1: 2, 20: 21}.values():  # [unbalanced-dict-unpacking]
    print(key)

one, *others = {1: 2, 3: 4, 5: 6}.items()
one, *others, last = {1: 2, 3: 4, 5: 6}.items()

one, *others = {1: 2, 3: 4, 5: 6}.values()
one, *others, last = {1: 2, 3: 4, 5: 6}.values()

_, *others = {1: 2, 3: 4, 5: 6}.items()
_, *others = {1: 2, 3: 4, 5: 6}.values()
_, others = {1: 2, 3: 4, 5: 6}.values()  # [unbalanced-dict-unpacking]
