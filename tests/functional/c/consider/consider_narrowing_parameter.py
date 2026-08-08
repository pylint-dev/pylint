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
    return fruit.color


def sum_prices(basket):  # [consider-narrowing-parameter]
    if not basket.prices:
        return 0
    return sum(basket.prices)


def first_value_name(node):  # [consider-narrowing-parameter]
    if node.value:
        return node.value.name
    return None


def compare(apple, banana):  # [consider-narrowing-parameter, consider-narrowing-parameter]
    if apple.weight == banana.weight:
        return 0
    return apple.weight - banana.weight


def make_color_getter(fruit):  # [consider-narrowing-parameter]
    def getter():
        return fruit.color

    print(fruit.color)
    return getter


def color_names(basket):  # [consider-narrowing-parameter]
    return sorted(color.name for color in basket.colors), len(basket.colors)


async def fetch_price(order):  # [consider-narrowing-parameter]
    print(order.price)
    return await order.price


def keyword_only(*, fruit):  # [consider-narrowing-parameter]
    print(fruit.color)
    return fruit.color


def mixed_call_and_read(basket):  # [consider-narrowing-parameter]
    basket.update()
    return basket.update


def shadowing(fruit):
    def inner(fruit):  # [consider-narrowing-parameter]
        print(fruit.taste)
        return fruit.taste

    print(fruit.color)
    return inner(fruit)


def called_directly(fruit):  # [consider-narrowing-parameter]
    print(fruit.color)
    return fruit.color


VALUE = called_directly(Kiwi())


class Basket:
    def __init__(self, fruit):  # [consider-narrowing-parameter]
        self.color = fruit.color
        self.loud_color = fruit.color.upper()

    def describe(self, fruit):  # [consider-narrowing-parameter]
        print(fruit.color)
        return f"a {fruit.color} fruit"

    @staticmethod
    def static_describe(fruit):  # [consider-narrowing-parameter]
        print(fruit.color)
        return fruit.color

    @classmethod
    def class_describe(cls, fruit):  # [consider-narrowing-parameter]
        print(fruit.color)
        return fruit.color


def single_access(fruit):
    return fruit.color


def duck_typed_filter(record):
    # A single access: typical of a short adapter implementing a duck-typed
    # interface, like 'filter(record)' for the logging framework.
    return record.origin


def escaped_callback(fruit):
    print(fruit.color)
    return fruit.color


CALLBACKS = [escaped_callback]


class LogFilter:
    def __init__(self):
        self.handlers = []

    def matches(self, record):
        print(record.origin)
        return record.origin

    def install(self):
        self.handlers.append(self.matches)


def bare_use(fruit):
    print(fruit.color)
    print(fruit.color)
    return fruit  # the whole object is needed


def two_attributes(fruit):
    print(fruit.color, fruit.color)
    return fruit.color, fruit.taste


def attribute_store(fruit):
    print(fruit.color)
    fruit.color = "red"


def attribute_delete(fruit):
    print(fruit.color)
    del fruit.color


def rebound(fruit):
    print(fruit.color)
    fruit = pick_fruit()
    return fruit.color


def deleted(fruit):
    color = fruit.color, fruit.color
    del fruit
    return color


def walrus(fruit):
    print(fruit.color)
    if fruit := pick_fruit():
        return fruit.color
    return None


def totally_unused(fruit):
    return "no fruit needed"


def only_method_calls(basket):
    basket.append("apple")
    basket.append("banana")


def cb_press(event):
    print(event.data)
    return event.data


def press_cb(event):
    print(event.data)
    return event.data


def variadic(*fruits, **options):
    print(fruits.index, options.keys)
    return fruits.index, options.keys


def ignored_names(_fruit, ignored_fruit, unused_fruit):
    print(_fruit.color, ignored_fruit.color, unused_fruit.color)
    return _fruit.color, ignored_fruit.color, unused_fruit.color


@lru_cache
def cached_color(fruit):
    print(fruit.color)
    return fruit.color


@singledispatch
def process(item):
    print(item.value)
    return item.value


class Fruit:
    def describe(self, sticker):
        return sticker.label, sticker.color


class Apple(Fruit):
    def describe(self, sticker):  # signature imposed by the parent class
        print(sticker.label)
        return sticker.label


class Sketch(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, shape):
        print(shape.outline)
        return shape.outline


class Template:
    def render(self, page):
        raise NotImplementedError(page.name + page.name)


class Reader(Protocol):
    def read(self, source):
        print(source.path)
        return source.path


class Weight:
    def __eq__(self, other):
        print(other.grams)
        return other.grams == 42


class Colored:
    @property
    def color(self):
        return self._hue

    @color.setter
    def color(self, value):
        self._hue = value.color
        self._dark_hue = value.color.lower()


def method_to_attach(self):
    """'self' follows the method convention even outside a class body."""
    print(self.color)
    return self.color


def class_factory(cls):
    """Same convention for 'cls'."""
    print(cls.color)
    return cls.color


def stamp_color(fruit, enabled):
    # An exit point precedes every access: narrowing would evaluate
    # 'fruit.color' unconditionally at the call site, which changes behavior
    # if the attribute is a property with side effects.
    if not enabled:
        return
    print(fruit.color)
    print(fruit.color)


def crash_line(report):
    # The code treats the attribute as possibly missing: hoisting the access
    # out of the 'try' would move the failure past the guard.
    try:
        print(report.summary)
        return str(report.summary)
    except AttributeError:
        return ""


def parse_weight(fruit):  # [consider-narrowing-parameter]
    # A handler that cannot catch AttributeError does not prevent narrowing.
    try:
        print(fruit.weight)
        return int(fruit.weight)
    except ValueError:
        return 0


class BaseJuicer:
    def squeeze(self, press):
        # Overridden by CitrusJuicer below: narrowing the base would break
        # the polymorphic call sites shared with the override.
        print(press.level)
        return press.level


class CitrusJuicer(BaseJuicer):
    def squeeze(self, press):
        print(press.level)
        return press.level * 2
