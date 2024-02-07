# pylint: disable=missing-docstring, import-error

from magic import shazam, turbogen


def bad(generator):
    for item in generator:
        yield item  # [use-yield-from]


def out_of_names():
    for item in turbogen():
        yield item  # [use-yield-from]


def good(generator):
    for item in generator:
        shazam()
        yield item


def yield_something():
    yield 5
