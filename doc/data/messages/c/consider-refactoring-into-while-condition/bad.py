fruit_basket = ["apple", "orange", "banana", "cherry", "guava"]

while True:  # [consider-refactoring-into-while-condition]
    if len(fruit_basket) == 0:
        break
    fruit = fruit_basket.pop()
    print(f"We removed {fruit} from the basket")
