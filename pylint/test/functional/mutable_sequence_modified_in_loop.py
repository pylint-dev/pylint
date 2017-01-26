items = range(1, 6)
for item in items:
    print(item)
    items.remove(item)

items = range(1, 6)
for item in items:
    print(item)
    items.pop(item)

items = range(1, 6)
for item in list(items):
    print(item)
    items.remove(item)


items = range(1, 6)
for item in items:
    print(item)
    items.remove(item)

items = range(1, 6)
for item in items:
    if True:
        items.remove(item)
        if True:
            items.pop()
    print(item)
