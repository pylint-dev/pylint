# A generator: it can only be looped over once, then it is empty
fruits = (name.upper() for name in ["apple", "banana"])
for basket in ["red basket", "blue basket"]:
    for fruit in fruits:  # [looping-through-iterator]
        print(basket, fruit)
