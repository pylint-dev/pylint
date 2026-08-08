"""With the default configuration only private and nested functions are checked."""

# pylint: disable=missing-docstring,too-few-public-methods


def public_price(basket):
    print(basket.price)
    return basket.price


def _private_price(basket):  # [consider-narrowing-parameter]
    print(basket.price)
    return basket.price


def outer_price(basket):
    def inner(fruit):  # [consider-narrowing-parameter]
        print(fruit.color)
        return fruit.color

    print(basket.price)
    return basket.price, inner(basket)


class Shop:
    def __init__(self, fruit):
        # dunders are part of the public interface of the class
        self.color = fruit.color
        self.dark = fruit.color

    def banner(self, fruit):
        print(fruit.color)
        return fruit.color

    def _sticker(self, fruit):  # [consider-narrowing-parameter]
        print(fruit.color)
        return fruit.color
