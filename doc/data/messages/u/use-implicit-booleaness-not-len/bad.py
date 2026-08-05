fruits = ["orange", "apple"]

if len(fruits):  # [use-implicit-booleaness-not-len]
    print(fruits)

# Now also catches comparisons with zero
if len(fruits) == 0:  # [use-implicit-booleaness-not-len]
    print("empty")

if len(fruits) > 0:  # [use-implicit-booleaness-not-len]
    print("has items")

if len(fruits) != 0:  # [use-implicit-booleaness-not-len]
    print("not empty")
