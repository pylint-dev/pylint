fruits = {"apple": 1, "orange": 2, "mango": 3}

i = 0
for fruit in fruits:
    fruits["apple"] = i  # [modified-iterating-dict]
    i += 1
