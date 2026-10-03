def pick_fruits(fruits):
    for fruit in fruits:
        print(fruit)

    return []


pick_fruits(["apple"])[0] = "orange"
