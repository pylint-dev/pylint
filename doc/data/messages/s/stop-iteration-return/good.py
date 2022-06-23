def fruit_generator():
    """The example is simple enough you don't need an explicit return."""
    for fruit in ["apple", "banana"]:
        yield fruit


def two_fruits_generator(fruits):
    """Catching the StopIteration."""
    for fruit in fruits:
        try:
            yield fruit, next(fruits)
        except StopIteration:
            print("Sorry there is only one fruit left.")
            yield fruit, None


def two_good_fruits_generator(fruits):
    """A return can be used to end the iterator early, but not a StopIteration."""
    for fruit in fruits:
        if not fruit.is_tasty():
            continue
        while True:
            next_fruit = next(fruits, None)
            if next_fruit is None:
                print("Sorry there is only one fruit left.")
                yield fruit, None
                # We reached the end of the 'fruits' generator but raising a
                # StopIteration instead of returning would create a RuntimeError
                return
            if next_fruit.is_tasty():
                yield fruit, next_fruit
                break
