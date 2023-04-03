def pick_fruits(fruits):
    for fruit in fruits:
        print(fruit)


pick_fruits(["apple"])[0] = "orange"  # [unsupported-assignment-operation]
