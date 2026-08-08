"""Tests for consider-narrowing-parameter."""

# pylint: disable=missing-docstring,too-few-public-methods,unused-argument

from abc import ABCMeta, abstractmethod
from functools import lru_cache, singledispatch
from typing import Protocol


class Kiwi:
    color = "green"


def pick_fruit():
    return Kiwi()


def print_color(fruit):  # [consider-narrowing-parameter]
    print(fruit.color)


def sum_prices(basket):  # [consider-narrowing-parameter]
    total = 0
    for price in basket.prices:
        total += price
    return total


def first_value_name(node):  # [consider-narrowing-parameter]
    if node.value:
        return node.value.name
    return None


def compare(apple, banana):  # [consider-narrowing-parameter, consider-narrowing-parameter]
    return apple.weight > banana.weight


def make_color_getter(fruit):  # [consider-narrowing-parameter]
    def getter():
        return fruit.color

    return getter


def color_names(basket):  # [consider-narrowing-parameter]
    return [color.name for color in basket.colors]


async def fetch_price(order):  # [consider-narrowing-parameter]
    return await order.price


def keyword_only(*, fruit):  # [consider-narrowing-parameter]
    return fruit.color


def mixed_call_and_read(basket):  # [consider-narrowing-parameter]
    basket.update()
    return basket.update


def shadowing(fruit):
    def inner(fruit):  # [consider-narrowing-parameter]
        return fruit.taste

    print(fruit.color)
    return fruit, inner


class Basket:
    def __init__(self, fruit):  # [consider-narrowing-parameter]
        self.color = fruit.color

    def describe(self, fruit):  # [consider-narrowing-parameter]
        return f"a {fruit.color} fruit"

    @staticmethod
    def static_describe(fruit):  # [consider-narrowing-parameter]
        return fruit.color

    @classmethod
    def class_describe(cls, fruit):  # [consider-narrowing-parameter]
        return fruit.color


def bare_use(fruit):
    print(fruit.color)
    return fruit  # the whole object is needed


def two_attributes(fruit):
    return fruit.color, fruit.taste


def attribute_store(fruit):
    fruit.color = "red"


def attribute_delete(fruit):
    del fruit.color


def rebound(fruit):
    fruit = pick_fruit()
    return fruit.color


def deleted(fruit):
    color = fruit.color
    del fruit
    return color


def walrus(fruit):
    if fruit := pick_fruit():
        return fruit.color
    return None


def totally_unused(fruit):
    return "no fruit needed"


def only_method_calls(basket):
    basket.append("apple")
    basket.append("banana")


def cb_press(event):
    return event.data


def press_cb(event):
    return event.data


def variadic(*fruits, **options):
    return fruits.index, options.keys


def ignored_names(_fruit, ignored_fruit, unused_fruit):
    return _fruit.color, ignored_fruit.color, unused_fruit.color


@lru_cache
def cached_color(fruit):
    return fruit.color


@singledispatch
def process(item):
    return item.value


class Fruit:
    def describe(self, sticker):
        return sticker.label, sticker.color


class Apple(Fruit):
    def describe(self, sticker):  # signature imposed by the parent class
        return sticker.label


class Sketch(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, shape):
        return shape.outline


class Template:
    def render(self, page):
        raise NotImplementedError(page.name)


class Reader(Protocol):
    def read(self, source):
        return source.path


class Weight:
    def __eq__(self, other):
        return other.grams == 42


class Colored:
    @property
    def color(self):
        return self._hue

    @color.setter
    def color(self, value):
        self._hue = value.color


def method_to_attach(self):
    """'self' follows the method convention even outside a class body."""
    return self.color


def class_factory(cls):
    """Same convention for 'cls'."""
    return cls.color
