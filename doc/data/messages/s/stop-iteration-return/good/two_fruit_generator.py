def two_fruits_generator(fruits):
    """Catching the StopIteration."""
    for fruit in fruits:
        try:
            yield fruit, next(fruits)
        except StopIteration:
            print("Sorry there is only one fruit left.")
            yield fruit, None
