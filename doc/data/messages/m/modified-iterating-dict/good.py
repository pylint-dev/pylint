fruits = {"apple": 1, "orange": 2, "mango": 3}

i = 0
for fruit in fruits.copy():
    fruits["apple"] = i
    i += 1
