def two_fruits_generator(fruits):
    for fruit in fruits:
        yield fruit, next(fruits)  # [stop-iteration-return]
