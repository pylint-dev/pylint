# pylint: disable=missing-docstring,invalid-name
def gen1():
    yield 1
    yield 2
    yield 3
    raise StopIteration  # [stopiteration-raised-in-gen]


def gen2():
    yield from gen1()
