# Looks like a tuple, but it is a generator: it can only be looped over once
fruits = (name.upper() for name in ["apple", "banana"])
for basket in ["red basket", "blue basket"]:
    for fruit in fruits:  # [looping-through-iterator]
        print(basket, fruit)
