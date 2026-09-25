# A list: it can be looped over again and again
fruits = [name.upper() for name in ["apple", "banana"]]
for basket in ["red basket", "blue basket"]:
    for fruit in fruits:
        print(basket, fruit)
