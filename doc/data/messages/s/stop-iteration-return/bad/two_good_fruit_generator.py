def two_good_fruits_generator(fruits):
    for fruit in fruits:
        if not fruit.is_tasty():
            continue
        while True:
            next_fruit = next(fruits)  # [stop-iteration-return]
            if next_fruit.is_tasty():
                yield fruit, next_fruit
                break
