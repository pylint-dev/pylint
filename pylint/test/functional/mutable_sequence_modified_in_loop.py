""" The mutable sequence was modified inside the loop """

# pylint:disable=superfluous-parens,using-constant-test,invalid-name,missing-docstring

items = range(1, 6)
for item in items:
    print(item)
    items.remove(item)  # [mutable-sequence-modified-in-loop]

items = range(1, 6)
for item in items:
    print(item)
    items.pop(item)  # [mutable-sequence-modified-in-loop]

items = range(1, 6)
for item in list(items):
    print(item)
    items.remove(item)


items = range(1, 6)
for item in items:
    print(item)
    items.remove(item)  # [mutable-sequence-modified-in-loop]

items = range(1, 6)
for item in items:
    if True:
        items.remove(item)  # [mutable-sequence-modified-in-loop]
        if True:
            items.pop()  # [mutable-sequence-modified-in-loop]
    print(item)
